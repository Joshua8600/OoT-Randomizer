from typing import TYPE_CHECKING, Optional, Tuple, List, Dict, Union, Iterable, Set, Any, Callable

from ItemList import item_table
from RulesCommon import allowed_globals, escape_name

if TYPE_CHECKING:
    from Location import Location
    from World import World


class ItemInfo:
    items: 'Dict[str, ItemInfo]' = {}
    events: 'Dict[str, ItemInfo]' = {}
    bottles: Set[str] = set()
    medallions: Set[str] = set()
    stones: Set[str] = set()
    junk: Dict[str, int] = {}

    solver_ids: Dict[str, int] = {}
    bottle_ids: Set[int] = set()
    medallion_ids: Set[int] = set()
    stone_ids: Set[int] = set()

    def __init__(self, name: str = '', event: bool = False) -> None:
        if event:
            item_type = 'Event'
            progressive = True
            item_id = None
            special = None
        else:
            (item_type, progressive, item_id, special) = item_table[name]

        self.name: str = name
        self.advancement: bool = (progressive is True)
        self.priority: bool = (progressive is False)
        self.type: str = item_type
        self.special: Dict[str, Any] = special or {}
        self.index: Optional[int] = item_id
        self.price: Optional[int] = self.special.get('price', None)
        self.bottle: bool = self.special.get('bottle', False)
        self.medallion: bool = self.special.get('medallion', False)
        self.stone: bool = self.special.get('stone', False)
        self.alias: Optional[Tuple[str, int]] = self.special.get('alias', None)
        self.junk: Optional[int] = self.special.get('junk', None)
        self.trade: bool = self.special.get('trade', False)

        self.solver_id = None
        if name and self.junk is None:
            esc = escape_name(name)
            if esc not in ItemInfo.solver_ids:
                allowed_globals[esc] = ItemInfo.solver_ids[esc] = len(ItemInfo.solver_ids)
            self.solver_id = ItemInfo.solver_ids[esc]


for item_name in item_table:
    ItemInfo.items[item_name] = ItemInfo(item_name)
    if ItemInfo.items[item_name].bottle:
        ItemInfo.bottles.add(item_name)
        ItemInfo.bottle_ids.add(ItemInfo.solver_ids[escape_name(item_name)])
    if ItemInfo.items[item_name].medallion:
        ItemInfo.medallions.add(item_name)
        ItemInfo.medallion_ids.add(ItemInfo.solver_ids[escape_name(item_name)])
    if ItemInfo.items[item_name].stone:
        ItemInfo.stones.add(item_name)
        ItemInfo.stone_ids.add(ItemInfo.solver_ids[escape_name(item_name)])
    if ItemInfo.items[item_name].junk is not None:
        ItemInfo.junk[item_name] = ItemInfo.items[item_name].junk


class Item:
    def __init__(self, name: str = '', world: "Optional[World]" = None, event: bool = False) -> None:
        self.name: str = name
        self.location: "Optional[Location]" = None
        self.event: bool = event
        if event:
            if name not in ItemInfo.events:
                ItemInfo.events[name] = ItemInfo(name, event=True)
            self.info: ItemInfo = ItemInfo.events[name]
        else:
            self.info: ItemInfo = ItemInfo.items[name]
        self.price: Optional[int] = self.info.special.get('price', None)
        self.world: "World" = world
        self.looks_like_item: 'Optional[Item]' = None
        self.advancement: bool = self.info.advancement
        self.priority: bool = self.info.priority
        self.type: str = self.info.type
        self.special: dict = self.info.special
        self.index: Optional[int] = self.info.index
        self.alias: Optional[Tuple[str, int]] = self.info.alias

        self.solver_id = self.info.solver_id
        # Do not alias to junk--it has no solver id!
        self.alias_id = ItemInfo.solver_ids[escape_name(self.alias[0])] if self.alias else None

    item_worlds_to_fix: 'Dict[Item, int]' = {}

    def copy(self, new_world: "Optional[World]" = None) -> 'Item':
        if new_world is not None and self.world is not None and new_world.id != self.world.id:
            new_world = None

        new_item = Item(self.name, new_world, self.event)
        new_item.price = self.price

        if new_world is None and self.world is not None:
            Item.item_worlds_to_fix[new_item] = self.world.id

        return new_item

    @classmethod
    def fix_worlds_after_copy(cls, worlds: "List[World]") -> None:
        items_fixed = []
        for item, world_id in cls.item_worlds_to_fix.items():
            item.world = worlds[world_id]
            items_fixed.append(item)
        for item in items_fixed:
            del cls.item_worlds_to_fix[item]

    @property
    def key(self) -> bool:
        return self.smallkey or self.bosskey

    @property
    def smallkey(self) -> bool:
        return self.type == 'SmallKey' or self.type == 'HideoutSmallKey' or  self.type == 'TCGSmallKey'

    @property
    def bosskey(self) -> bool:
        return self.type == 'BossKey' or self.type == 'GanonBossKey'

    @property
    def map(self) -> bool:
        return self.type == 'Map'

    @property
    def compass(self) -> bool:
        return self.type == 'Compass'

    @property
    def dungeonitem(self) -> bool:
        return self.smallkey or self.bosskey or self.map or self.compass or self.type == 'SilverRupee'

    @property
    def unshuffled_dungeon_item(self) -> bool:
        return ((self.type == 'SmallKey' and self.world.settings.shuffle_smallkeys in ('remove', 'vanilla', 'dungeon')) or
                (self.type == 'HideoutSmallKey' and self.world.settings.shuffle_hideoutkeys == 'vanilla') or
                (self.type == 'TCGSmallKey' and self.world.settings.shuffle_tcgkeys in ('remove', 'vanilla')) or
                (self.type == 'BossKey' and self.world.settings.shuffle_bosskeys in ('remove', 'vanilla', 'dungeon')) or
                (self.type == 'GanonBossKey' and self.world.settings.shuffle_ganon_bosskey in ('remove', 'vanilla', 'dungeon')) or
                ((self.map or self.compass) and (self.world.settings.shuffle_mapcompass in ('remove', 'startwith', 'vanilla', 'dungeon'))) or
                (self.type == 'SilverRupee' and self.world.settings.shuffle_silver_rupees in ['remove','vanilla','dungeon']))

    @property
    def majoritem(self) -> bool:
        if self.type == 'Token':
            return (self.world.settings.bridge == 'tokens' or self.world.settings.shuffle_ganon_bosskey == 'tokens' or
                (self.world.settings.shuffle_ganon_bosskey == 'on_lacs' and self.world.settings.lacs_condition == 'tokens'))

        if self.type in ('Drop', 'Event', 'Shop', 'DungeonReward') or not self.advancement:
            return False

        if self.name.startswith('Bombchus') and not self.world.settings.free_bombchu_drops:
            return False

        if self.name == 'Heart Container' or self.name.startswith('Piece of Heart'):
            return (self.world.settings.bridge == 'hearts' or self.world.settings.shuffle_ganon_bosskey == 'hearts' or
                (self.world.settings.shuffle_ganon_bosskey == 'on_lacs' and self.world.settings.lacs_condition == 'hearts'))

        if self.map or self.compass:
            return False
        if self.type == 'SmallKey' and self.world.settings.shuffle_smallkeys in ['dungeon', 'vanilla']:
            return False
        if self.type == 'HideoutSmallKey' and self.world.settings.shuffle_hideoutkeys == 'vanilla':
            return False
        if self.type == 'TCGSmallKey' and self.world.settings.shuffle_tcgkeys == 'vanilla':
            return False
        if self.type == 'BossKey' and self.world.settings.shuffle_bosskeys in ['dungeon', 'vanilla']:
            return False
        if self.type == 'GanonBossKey' and self.world.settings.shuffle_ganon_bosskey in ['dungeon', 'vanilla']:
            return False
        if self.type == 'SilverRupee' and self.world.settings.shuffle_silver_rupees in ['dungeon', 'vanilla']:
            return False

        return True

    @property
    def goalitem(self) -> bool:
        return self.name in self.world.goal_items

    def __str__(self) -> str:
        return str(self.__unicode__())

    def __unicode__(self) -> str:
        return '%s' % self.name


def ItemFactory(items: Union[str, Iterable[str]], world: "Optional[World]" = None, event: bool = False) -> Union[Item, List[Item]]:
    if isinstance(items, str):
        if not event and items not in ItemInfo.items:
            raise KeyError('Unknown Item: %s' % items)
        return Item(items, world, event)

    ret = []
    for item in items:
        if not event and item not in ItemInfo.items:
            raise KeyError('Unknown Item: %s' % item)
        ret.append(Item(item, world, event))

    return ret


def make_event_item(name: str, location: "Location", item: Optional[Item] = None) -> Item:
    if item is None:
        item = Item(name, location.world, event=True)
    location.world.push_item(location, item)
    location.locked = True
    if name not in item_table:
        location.internal = True
    location.world.event_items.add(name)
    return item


def is_item(name: str) -> bool:
    return name in item_table


def ItemIterator(predicate: Callable[[Item], bool] = lambda item: True, world: "Optional[World]" = None) -> Iterable[Item]:
    for item_name in item_table:
        item = ItemFactory(item_name, world)
        if predicate(item):
            yield item
