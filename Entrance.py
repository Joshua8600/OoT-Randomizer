from typing import TYPE_CHECKING, List, Optional, Callable, Dict, Any

from RulesCommon import AccessRule

if TYPE_CHECKING:
    from Region import Region
    from World import World


class Entrance:
    def __init__(self, name: str = '', parent: "Optional[Region]" = None) -> None:
        self.name: str = name
        self.parent_region: "Optional[Region]" = parent
        self.world: "World" = parent.world
        self.connected_region: "Optional[Region]" = None
        self.access_rule: AccessRule = lambda state, **kwargs: True
        self.access_rules: List[AccessRule] = []
        self.reverse: 'Optional[Entrance]' = None
        self.replaces: 'Optional[Entrance]' = None
        self.assumed: 'Optional[Entrance]' = None
        self.type: Optional[str] = None
        self.shuffled: bool = False
        self.data: Optional[Dict[str, Any]] = None
        self.primary: bool = False
        self.always: bool = False
        self.never: bool = False
        self.rule_string: Optional[str] = None

    def copy(self, new_region: "Region") -> 'Entrance':
        new_entrance = Entrance(self.name, new_region)
        new_entrance.connected_region = self.connected_region.name
        new_entrance.access_rule = self.access_rule
        new_entrance.access_rules = list(self.access_rules)
        new_entrance.reverse = self.reverse
        new_entrance.replaces = self.replaces
        new_entrance.assumed = self.assumed
        new_entrance.type = self.type
        new_entrance.shuffled = self.shuffled
        new_entrance.data = self.data
        new_entrance.primary = self.primary
        new_entrance.always = self.always
        new_entrance.never = self.never

        return new_entrance

    def add_rule(self, lambda_rule: AccessRule) -> None:
        if self.always:
            self.set_rule(lambda_rule)
            self.always = False
            return
        if self.never:
            return
        self.access_rules.append(lambda_rule)
        self.access_rule = lambda state, **kwargs: all(rule(state, **kwargs) for rule in self.access_rules)

    def set_rule(self, lambda_rule: AccessRule) -> None:
        self.access_rule = lambda_rule
        self.access_rules = [lambda_rule]

    def connect(self, region: "Region") -> None:
        self.connected_region = region
        region.entrances.append(self)

    def disconnect(self) -> "Optional[Region]":
        self.connected_region.entrances.remove(self)
        previously_connected = self.connected_region
        self.connected_region = None
        return previously_connected

    def bind_two_way(self, other_entrance: 'Entrance') -> None:
        self.reverse = other_entrance
        other_entrance.reverse = self

    def get_new_target(self) -> 'Entrance':
        root = self.world.get_region('Root Exits')
        target_entrance = Entrance('Root -> ' + self.connected_region.name, root)
        target_entrance.connect(self.connected_region)
        target_entrance.replaces = self
        root.exits.append(target_entrance)
        return target_entrance

    def assume_reachable(self) -> 'Entrance':
        if self.assumed is None:
            self.assumed = self.get_new_target()
            self.disconnect()
        return self.assumed

    def __str__(self) -> str:
        return str(self.__unicode__())

    def __unicode__(self) -> str:
        return '%s' % self.name
