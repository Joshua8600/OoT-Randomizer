from __future__ import annotations
from enum import Enum
from ProcessActors import Actor, Scene
import Rom

# Location specific restriction constants. Enemies must be tagged w/ these in order to be placed at this location
class LOCATION_RESTRICTION(Enum):
    UNDERWATER = 1 # Underwater locations - generally an enemy that requires hookshot + iron boots
    FLOATING = 2 # Locations that require an enemy that can float. Like because it's over a pit or something.
    ABOVE_GROUND = 3 # Locations that the enemy will spawn above the ground, only place enemies that will automatically move to the ground or won't break if they're in the air
    ABOVE_WATER = 4 # Location is above water and requires that the enemy  

# Enemy specific restrictions. Locations must be tagged w/ these in order for the enemy to be placed.
class ENEMY_RESTRICTION(Enum):
    ABOVE_WATER = 1
    OUTSIDE = 2
    INSIDE = 3

# Define an enemy location supporting restrictions
# restrictions - list of restrictions for this location. Enemy must have these restrictions tagged on them in order to spawn here. Ex. UNDERWATER
# meets_enemy_restrictions - list of enemy restrictions that this location meets. Ex. certain enemies can only spawn above water
# disallowed enemies - list of enemy types to explicitly disallow
# patch_func - function that will apply a ROM patch applicable to this location
class EnemyLocation:
    def __init__(self, vanilla_id, restrictions: list[LOCATION_RESTRICTION] = [], meets_enemy_restrictions: list[ENEMY_RESTRICTION] = [], disallowed_enemies: list[int] = [], patch_func = None, switch_flag = -1, skip_raycast = False):
        self.id = vanilla_id
        self.restrictions = restrictions
        self.meets_enemy_restrictions = meets_enemy_restrictions
        self.disallowed_enemies = disallowed_enemies
        self.patch_func = patch_func
        self.switch_flag = switch_flag
        self.skip_raycast = skip_raycast

# Move the SFM wolfos more towards the center, some enemies like flare dancer might jump over the fence
def patch_func_sfm_wolfos(actor: Actor):
    actor.x = -195
    actor.y = 0
    actor.z = 1900

# Move the stalfos in MQ Child spirit down onto the platform
def patch_mq_spirit_child_stalfos(actor: Actor):
    actor.y = 50

# Move the like likes in the room in MQ jabu to just spawn on the ground
# They normally spawn in cages above the room
def patch_mq_jabu_likelike_left(actor: Actor):
    actor.x = 827
    actor.y = -300

def patch_mq_jabu_likelike_right(actor: Actor):
    actor.x = 488
    actor.y = -300

base_enemy_list = {
    (10, 0, 0, 1):      EnemyLocation(37), # Lizalfos/Dinalfos
    (10, 0, 0, 2):      EnemyLocation(37), # Lizalfos/Dinalfos
    (10, 2, 0, 5):      EnemyLocation(2), # Stalfos
    (10, 2, 0, 6):      EnemyLocation(2), # Stalfos
    (10, 4, 0, 1):      EnemyLocation(275), # Iron Knuckle
    (10, 4, 0, 2):      EnemyLocation(275), # Iron Knuckle
    (10, 7, 0, 1):      EnemyLocation(19), # Keese
    (10, 7, 0, 2):      EnemyLocation(19), # Keese
    (10, 7, 0, 3):      EnemyLocation(19), # Keese
    (10, 7, 0, 4):      EnemyLocation(19), # Keese
    (10, 7, 0, 5):      EnemyLocation(19), # Keese
    (10, 7, 0, 6):      EnemyLocation(19), # Keese
    (10, 7, 0, 7):      EnemyLocation(19), # Keese
    (15, 0, 0, 4):      EnemyLocation(144), # Redead/Gibdo
    (23, 1, 0, 0):      EnemyLocation(275), # Iron Knuckle
    (34, 0, 0, 0):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 1):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 2):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 3):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 4):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 5):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 6):      EnemyLocation(144), # Redead/Gibdo
    (34, 0, 0, 7):      EnemyLocation(144), # Redead/Gibdo
    (62, 2, 0, 0):      EnemyLocation(144), # Redead/Gibdo
    (62, 2, 0, 1):      EnemyLocation(144), # Redead/Gibdo
    (62, 4, 0, 0):      EnemyLocation(55), # Skulltula
    (62, 5, 0, 0):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (62, 7, 0, 0):      EnemyLocation(431), # Wolfos
    (62, 7, 0, 1):      EnemyLocation(431), # Wolfos
    (62, 8, 0, 0):      EnemyLocation(149), # Skullwaltula
    (62, 8, 0, 1):      EnemyLocation(149), # Skullwaltula
    (62, 10, 0, 2):     EnemyLocation(27, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER]), # Tektite
    (62, 13, 0, 0):     EnemyLocation(55), # Skulltula
    (63, 0, 0, 1):      EnemyLocation(144), # Redead/Gibdo
    (65, 0, 0, 0):      EnemyLocation(19), # Keese
    (65, 0, 0, 1):      EnemyLocation(19), # Keese
    (65, 0, 0, 3):      EnemyLocation(19), # Keese
    (65, 0, 0, 4):      EnemyLocation(19), # Keese
    (65, 1, 0, 0):      EnemyLocation(144), # Redead/Gibdo
    (65, 1, 0, 1):      EnemyLocation(144), # Redead/Gibdo
    (65, 1, 0, 2):      EnemyLocation(144), # Redead/Gibdo
    (72, 2, 0, 3):      EnemyLocation(144), # Redead/Gibdo
    (72, 2, 0, 4):      EnemyLocation(144), # Redead/Gibdo
    (72, 3, 0, 2):      EnemyLocation(144), # Redead/Gibdo
    (72, 3, 0, 3):      EnemyLocation(144), # Redead/Gibdo
    (81, 0, 0, 8):      EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 9):      EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 10):     EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 11):     EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 12):     EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 13):     EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (81, 0, 0, 14):     EnemyLocation(29, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Peahat
    (83, 1, 2, 2):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 2, 3):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 2, 4):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 2, 5):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 2, 6):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 2, 7):      EnemyLocation(149,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skullwaltula
    (83, 1, 2, 8):      EnemyLocation(149,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skullwaltula
    (83, 1, 3, 2):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 3, 3):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 3, 4):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 3, 5):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 3, 6):      EnemyLocation(19, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Keese
    (83, 1, 3, 7):      EnemyLocation(149, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skullwaltula
    (83, 1, 3, 8):      EnemyLocation(149, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skullwaltula
    (84, 0, 2, 2):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 3):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 4):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 5):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 6):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 7):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 8):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 2, 9):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 0, 4):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 0, 5):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (84, 0, 0, 42):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (84, 0, 0, 43):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (85, 0, 2, 1):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (85, 0, 2, 2):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (85, 0, 2, 3):      EnemyLocation(55,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skulltula
    (85, 0, 2, 4):      EnemyLocation(96,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (85, 0, 2, 5):      EnemyLocation(96,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (85, 0, 2, 6):      EnemyLocation(96,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (85, 0, 2, 7):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 0, 2, 8):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 0, 2, 9):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 0, 2, 10):     EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 2):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 3):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 4):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 5):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 6):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 2, 7):      EnemyLocation(85,meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Baba
    (85, 1, 0, 1):      EnemyLocation(199, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Whithered Deku Baba
    (85, 1, 0, 2):      EnemyLocation(199, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Whithered Deku Baba
    (85, 1, 0, 3):      EnemyLocation(199, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Whithered Deku Baba
    (85, 1, 0, 4):      EnemyLocation(199, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Whithered Deku Baba
    (85, 1, 0, 5):      EnemyLocation(199, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Whithered Deku Baba
    (86, 0, 2, 5):      EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 2, 6):      EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 2, 7):      EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 2, 8):      EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 2, 9):      EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 2, 10):     EnemyLocation(75, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Moblin
    (86, 0, 0, 1):      EnemyLocation(431, switch_flag=0x1F, patch_func=patch_func_sfm_wolfos), # Wolfos. Move the spawn point so certain enemies don't end up on the other side of the gate.
    (86, 0, 0, 5):      EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (86, 0, 0, 6):      EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (86, 0, 0, 7):      EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (86, 0, 0, 8):      EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (86, 0, 0, 9):      EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (86, 0, 0, 10):     EnemyLocation(96, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Deku Scrub
    (87, 0, 2, 15):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (87, 0, 2, 16):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (87, 0, 2, 17):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (87, 0, 2, 18):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (87, 0, 2, 22):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 23):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 24):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 25):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 26):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 27):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 28):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 2, 29):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (87, 0, 0, 3):      EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (87, 0, 0, 4):      EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (87, 0, 0, 5):      EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (87, 0, 0, 19):     EnemyLocation(27, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Tektite
    (87, 0, 0, 20):     EnemyLocation(27, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Tektite
    (87, 0, 0, 21):     EnemyLocation(27, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Tektite
    (89, 0, 2, 18):     EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (89, 0, 2, 19):     EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (89, 0, 2, 20):     EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (89, 0, 2, 21):     EnemyLocation(14, restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE], skip_raycast=True), # Octorok
    (89, 0, 2, 24):     EnemyLocation(55), # Skulltula
    (89, 0, 2, 25):     EnemyLocation(55), # Skulltula
    (89, 0, 2, 26):     EnemyLocation(55), # Skulltula
    (89, 0, 2, 27):     EnemyLocation(55), # Skulltula
    (89, 0, 2, 28):     EnemyLocation(55), # Skulltula
    (89, 0, 2, 50):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (90, 0, 2, 3):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (90, 0, 2, 4):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (90, 0, 2, 5):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (90, 0, 2, 6):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (90, 0, 2, 7):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
    (91, 1, 2, 1):      EnemyLocation(277, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skull Kid
    (91, 1, 2, 2):      EnemyLocation(277, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skull Kid
    (91, 3, 2, 2):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (91, 3, 0, 2):      EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER, ENEMY_RESTRICTION.OUTSIDE]), # Octorok
    (91, 9, 2, 1):      EnemyLocation(277, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Skull Kid
    (92, 0, 2, 7):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 2, 8):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 2, 9):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 2, 10):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 2, 11):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 0, 7):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 0, 8):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (92, 0, 0, 9):      EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (96, 0, 2, 2):      EnemyLocation(149), # Skullwaltula
    (96, 0, 2, 3):      EnemyLocation(149), # Skullwaltula
    (96, 0, 2, 4):      EnemyLocation(149), # Skullwaltula
    (96, 0, 2, 6):      EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 2, 7):      EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 2, 8):      EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 0, 6):      EnemyLocation(149), # Skullwaltula
    (96, 0, 0, 7):      EnemyLocation(149), # Skullwaltula
    (96, 0, 0, 8):      EnemyLocation(149), # Skullwaltula
    (96, 0, 0, 9):      EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 0, 10):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 0, 11):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (96, 0, 0, 12):     EnemyLocation(27, meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Tektite
    (97, 1, 2, 8):      EnemyLocation(105), # Bubble
    (97, 1, 2, 9):      EnemyLocation(105), # Bubble
    (97, 1, 2, 10):     EnemyLocation(105), # Bubble
    (97, 1, 2, 11):     EnemyLocation(105), # Bubble
    (97, 1, 2, 12):     EnemyLocation(105), # Bubble
    (99, 0, 1, 10):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 11):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 12):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 13):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 14):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 15):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 16):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 17):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 18):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 19):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 20):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 21):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 22):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 23):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
    (99, 0, 1, 24):     EnemyLocation(448, restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], meets_enemy_restrictions=[ENEMY_RESTRICTION.OUTSIDE]), # Guay
}

base_enemy_alts = {
    (81,0,0,8):[(81,0,1,4)], # Peahat
    (81,0,0,12):[(81,0,1,8)], # Peahat
    (81,0,0,9):[(81,0,1,5)], # Peahat
    (81,0,0,10):[(81,0,1,6)], # Peahat
    (81,0,0,11):(81,0,1,7), # Peahat
    (81,0,0,14):(81,0,1,10), # Peahat
    (81,0,0,15):(81,0,1,9), # Peahat
}

vanilla_dungeon_enemies = {
    'Deku Tree': {
        (0, 0, 0, 0): 149, # Skullwaltula
        (0, 0, 0, 1): 149, # Skullwaltula
        (0, 0, 0, 2): 149, # Skullwaltula
        (0, 0, 0, 3): 55, # Skulltula
        (0, 0, 0, 4): 55, # Skulltula
        (0, 0, 0, 5): 55, # Skulltula
        (0, 0, 0, 11): 85, # Deku Baba
        (0, 0, 0, 12): 85, # Deku Baba
        (0, 0, 0, 13): 85, # Deku Baba
        (0, 3, 0, 0): 199, # Whithered Deku Baba
        (0, 3, 0, 3): 85, # Deku Baba
        (0, 3, 0, 4): 85, # Deku Baba
        (0, 3, 0, 5): 85, # Deku Baba
        (0, 5, 0, 0): 55, # Skulltula
        (0, 6, 0, 0): 199, # Whithered Deku Baba
        (0, 6, 0, 1): 199, # Whithered Deku Baba
        (0, 6, 0, 4): 85, # Deku Baba
        (0, 7, 0, 0): 199, # Whithered Deku Baba
        (0, 7, 0, 1): 55, # Skulltula
        (0, 7, 0, 4): 85, # Deku Baba
        (0, 7, 0, 5): 43, # Gohma Larva
        (0, 7, 0, 6): 43, # Gohma Larva
        (0, 7, 0, 7): 43, # Gohma Larva
        (0, 8, 0, 0): 55, # Skulltula
        (0, 10, 0, 0): 199, # Whithered Deku Baba
        (0, 10, 0, 1): 55, # Skulltula
        (0, 10, 0, 4): 85, # Deku Baba
    },
    'Dodongos Cavern': {
        (1, 0, 0, 5): 19, # Keese
        (1, 0, 0, 6): 19, # Keese
        (1, 0, 0, 7): 138, # Beamos
        (1, 0, 0, 8): 138, # Beamos
        (1, 0, 0, 9): 138, # Beamos
        (1, 1, 0, 0): 19, # Keese
        (1, 1, 0, 1): 19, # Keese
        (1, 1, 0, 2): 47, # Baby Dodongo
        (1, 1, 0, 3): 47, # Baby Dodongo
        (1, 1, 0, 4): 47, # Baby Dodongo
        (1, 1, 0, 5): 47, # Baby Dodongo
        (1, 1, 0, 6): 47, # Baby Dodongo
        (1, 1, 0, 7): 47, # Baby Dodongo
        (1, 2, 0, 0): 149, # Skullwaltula
        (1, 3, 0, 1): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 2): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 3): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 4): 37, # Lizalfos/Dinalfos
        (1, 4, 0, 0): 18, # Dodongo
        (1, 4, 0, 1): 18, # Dodongo
        (1, 4, 0, 2): 18, # Dodongo
        (1, 5, 0, 0): 84, # Armos
        (1, 5, 0, 1): 84, # Armos
        (1, 5, 0, 2): 84, # Armos
        (1, 5, 0, 3): 19, # Keese
        (1, 5, 0, 4): 19, # Keese
        (1, 7, 0, 1): 19, # Keese
        (1, 7, 0, 2): 19, # Keese
        (1, 8, 0, 0): 19, # Keese
        (1, 8, 0, 1): 19, # Keese
        (1, 10, 0, 1): 47, # Baby Dodongo
        (1, 10, 0, 2): 47, # Baby Dodongo
        (1, 10, 0, 3): 47, # Baby Dodongo
        (1, 11, 0, 0): 19, # Keese
        (1, 11, 0, 1): 19, # Keese
        (1, 11, 0, 2): 19, # Keese
        (1, 14, 0, 0): 84, # Armos
        (1, 15, 0, 0): 84, # Armos
    },
    'Jabu Jabus Belly': {
        (2, 0, 0, 0): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 0, 0, 1): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 0, 0, 3): 45, # Shabom
        (2, 0, 0, 4): 45, # Shabom
        (2, 1, 0, 0): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 1, 0, 1): 52, # Biri
        (2, 2, 0, 1): 99, # Bari
        (2, 2, 0, 2): 99, # Bari
        (2, 2, 0, 4): 52, # Biri
        (2, 2, 0, 5): 52, # Biri
        (2, 2, 0, 6): 52, # Biri
        (2, 3, 0, 1): 52, # Biri
        (2, 3, 0, 2): 52, # Biri
        (2, 3, 0, 3): 52, # Biri
        (2, 3, 0, 4): 52, # Biri
        (2, 4, 0, 0): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 5, 0, 1): 52, # Biri
        (2, 5, 0, 2): 52, # Biri
        (2, 5, 0, 3): 52, # Biri
        (2, 5, 0, 4): 52, # Biri
        (2, 5, 0, 5): 52, # Biri
        (2, 6, 0, 0): 52, # Biri
        (2, 6, 0, 1): 52, # Biri
        (2, 7, 0, 0): 53, # Tailpasaran
        (2, 7, 0, 1): 53, # Tailpasaran
        (2, 7, 0, 2): 53, # Tailpasaran
        (2, 7, 0, 3): 53, # Tailpasaran
        (2, 7, 0, 4): 53, # Tailpasaran
        (2, 8, 0, 1): 52, # Biri
        (2, 8, 0, 2): 52, # Biri
        (2, 8, 0, 3): 52, # Biri
        (2, 8, 0, 4): 52, # Biri
        (2, 9, 0, 0): 58, # Singray
        (2, 9, 0, 1): 58, # Singray
        (2, 9, 0, 2): 58, # Singray
        (2, 9, 0, 3): 58, # Singray
        (2, 12, 0, 2): 45, # Shabom
        (2, 12, 0, 3): 45, # Shabom
        (2, 12, 0, 4): 45, # Shabom
        (2, 12, 0, 5): 45, # Shabom
        (2, 12, 0, 6): 45, # Shabom
        (2, 12, 0, 7): 45, # Shabom
        (2, 12, 0, 8): 45, # Shabom
        (2, 12, 0, 9): 45, # Shabom
        (2, 12, 0, 10): 45, # Shabom
        (2, 13, 0, 0): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 13, 0, 1): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (2, 14, 0, 0): 58, # Singray
        (2, 14, 0, 1): 58, # Singray
        (2, 14, 0, 2): 58, # Singray
        (2, 14, 0, 10): 45, # Shabom
        (2, 14, 0, 11): 45, # Shabom
        (2, 14, 0, 12): 45, # Shabom
        (2, 14, 0, 13): 45, # Shabom
        (2, 14, 0, 14): 45, # Shabom
        (2, 14, 0, 15): 45, # Shabom
        (2, 14, 0, 16): 45, # Shabom
    },
    'Forest Temple': {
        (3, 0, 0, 0): 431, # Wolfos
        (3, 0, 0, 1): 431, # Wolfos
        (3, 1, 0, 0): 55, # Skulltula
        (3, 3, 0, 4): 55, # Skulltula
        (3, 4, 0, 0): 105, # Bubble
        (3, 5, 0, 4): 55, # Skulltula
        (3, 6, 0, 0): 2, # Stalfos
        (3, 6, 0, 1): 2, # Stalfos
        (3, 7, 0, 2): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (3, 7, 0, 3): 149, # Skullwaltula
        (3, 7, 0, 4): 85, # Deku Baba
        (3, 7, 0, 5): 85, # Deku Baba
        (3, 8, 0, 0): EnemyLocation(14, meets_enemy_restrictions=[ENEMY_RESTRICTION.ABOVE_WATER]), # Octorok
        (3, 8, 0, 1): 149, # Skullwaltula
        (3, 8, 0, 2): 149, # Skullwaltula
        (3, 8, 0, 3): 149, # Skullwaltula
        (3, 8, 0, 4): 85, # Deku Baba
        (3, 8, 0, 5): 85, # Deku Baba
        (3, 10, 0, 0): 105, # Bubble
        (3, 11, 0, 0): 105, # Bubble
        (3, 11, 0, 1): 105, # Bubble
        (3, 11, 0, 2): 105, # Bubble
        (3, 15, 0, 0): 55, # Skulltula
        (3, 15, 0, 1): 55, # Skulltula
        (3, 15, 0, 2): 55, # Skulltula
        (3, 17, 0, 0): 55, # Skulltula
        (3, 18, 0, 0): 142, # Floormaster
        (3, 19, 0, 0): EnemyLocation(17, skip_raycast=True), # Wallmaster
        (3, 20, 0, 0): EnemyLocation(105, skip_raycast=True), # Bubble
        (3, 20, 0, 1): EnemyLocation(105, skip_raycast=True), # Bubble
        (3, 20, 0, 2): EnemyLocation(17, skip_raycast=True), # Wallmaster
        (3, 21, 0, 0): 105, # Bubble
        (3, 21, 0, 1): 105, # Bubble
    },
    'Fire Temple': {
        (4, 0, 0, 0): 19, # Keese
        (4, 0, 0, 4): 19, # Keese
        (4, 1, 0, 1): 105, # Bubble
        (4, 1, 0, 3): 19, # Keese
        (4, 1, 0, 5): 105, # Bubble
        (4, 1, 0, 6): 19, # Keese
        (4, 1, 0, 8): 19, # Keese
        (4, 1, 0, 11): 105, # Bubble
        (4, 1, 0, 12): 105, # Bubble
        (4, 1, 0, 13): 105, # Bubble
        (4, 1, 0, 14): 105, # Bubble
        (4, 1, 0, 15): 105, # Bubble
        (4, 1, 0, 16): 105, # Bubble
        (4, 1, 0, 17): 19, # Keese
        (4, 1, 0, 22): 105, # Bubble
        (4, 3, 0, 0): 153, # Flare Dancer
        (4, 4, 0, 0): 56, # Torch Slug
        (4, 4, 0, 3): 56, # Torch Slug
        (4, 5, 0, 4): 56, # Torch Slug
        (4, 5, 0, 6): 56, # Torch Slug
        (4, 5, 0, 11): 56, # Torch Slug
        (4, 10, 0, 14): 19, # Keese
        (4, 10, 0, 25): 19, # Keese
        (4, 10, 0, 44): 19, # Keese
        (4, 13, 0, 2): 19, # Keese
        (4, 13, 0, 8): 19, # Keese
        (4, 13, 0, 9): 19, # Keese
        (4, 14, 0, 0): 19, # Keese
        (4, 14, 0, 1): 19, # Keese
        (4, 14, 0, 6): 19, # Keese
        (4, 14, 0, 7): 19, # Keese
        (4, 15, 0, 0): 19, # Keese
        (4, 15, 0, 1): 56, # Torch Slug
        (4, 15, 0, 2): 19, # Keese
        (4, 15, 0, 3): 56, # Torch Slug
        (4, 15, 0, 5): 56, # Torch Slug
        (4, 15, 0, 6): 19, # Keese
        (4, 15, 0, 7): 56, # Torch Slug
        (4, 16, 0, 0): 105, # Bubble
        (4, 16, 0, 1): 105, # Bubble
        (4, 16, 0, 2): 105, # Bubble
        (4, 16, 0, 3): 105, # Bubble
        (4, 16, 0, 4): 105, # Bubble
        (4, 18, 0, 0): 221, # Like like
        (4, 19, 0, 0): 221, # Like like
        (4, 21, 0, 0): 19, # Keese
        (4, 21, 0, 1): 19, # Keese
        (4, 21, 0, 3): 19, # Keese
        (4, 21, 0, 4): 19, # Keese
        (4, 24, 0, 0): 153, # Flare Dancer
    },
    'Water Temple': {
        (5, 0, 0, 2): 19, # Keese
        (5, 0, 0, 3): 19, # Keese
        (5, 0, 0, 4): 236, # Spike
        (5, 0, 0, 5): 236, # Spike
        (5, 0, 0, 12): 27, # Tektite
        (5, 0, 0, 13): 27, # Tektite
        (5, 2, 0, 0): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (5, 2, 0, 1): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (5, 2, 0, 2): EnemyLocation(236, [LOCATION_RESTRICTION.UNDERWATER], []), # Spike
        (5, 2, 0, 3): EnemyLocation(236, [LOCATION_RESTRICTION.UNDERWATER], []), # Spike
        (5, 2, 0, 4): EnemyLocation(236, [LOCATION_RESTRICTION.UNDERWATER], []), # Spike
        (5, 2, 0, 5): EnemyLocation(236, [LOCATION_RESTRICTION.UNDERWATER], []), # Spike
        (5, 2, 0, 6): EnemyLocation(236, [LOCATION_RESTRICTION.UNDERWATER], []), # Spike
        (5, 3, 0, 0): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (5, 3, 0, 2): 27, # Tektite
        (5, 3, 0, 3): 27, # Tektite
        (5, 4, 0, 1): EnemyLocation(396, [LOCATION_RESTRICTION.UNDERWATER]), # Stinger
        (5, 4, 0, 2): EnemyLocation(396, [LOCATION_RESTRICTION.UNDERWATER]), # Stinger
        (5, 4, 0, 3): EnemyLocation(396, [LOCATION_RESTRICTION.UNDERWATER]), # Stinger
        (5, 4, 0, 4): EnemyLocation(396, [LOCATION_RESTRICTION.UNDERWATER]), # Stinger
        (5, 5, 0, 3): 19, # Keese
        (5, 5, 0, 4): 19, # Keese
        (5, 6, 0, 0): 221, # Like like
        (5, 6, 0, 1): EnemyLocation(27), # Tektite
        (5, 6, 0, 2): EnemyLocation(27), # Tektite
        (5, 6, 0, 3): 27, # Tektite
        (5, 6, 0, 4): 27, # Tektite
        (5, 6, 0, 5): EnemyLocation(27), # Tektite
        (5, 8, 0, 2): 197, # Shell Blade
        (5, 8, 0, 3): 197, # Shell Blade
        (5, 9, 0, 0): 27, # Tektite
        (5, 10, 0, 1): 27, # Tektite
        (5, 12, 0, 0): 197, # Shell Blade
        (5, 12, 0, 3): 27, # Tektite
        (5, 12, 0, 4): 27, # Tektite
        (5, 12, 0, 5): 27, # Tektite
        (5, 12, 0, 6): 27, # Tektite
        (5, 12, 0, 7): 27, # Tektite
        (5, 12, 0, 8): 27, # Tektite
        (5, 14, 0, 0): 396, # Stinger
        (5, 14, 0, 1): 396, # Stinger
        (5, 14, 0, 2): 396, # Stinger
        (5, 14, 0, 3): 396, # Stinger
        (5, 14, 0, 4): 396, # Stinger
        (5, 15, 0, 0): 27, # Tektite
        (5, 15, 0, 1): 27, # Tektite
        (5, 18, 0, 0): 197, # Shell Blade
        (5, 18, 0, 1): 197, # Shell Blade
        (5, 18, 0, 2): 197, # Shell Blade
        (5, 19, 0, 0): 236, # Spike
        (5, 19, 0, 1): 236, # Spike
        (5, 19, 0, 2): 236, # Spike
        (5, 19, 0, 3): 236, # Spike
    },
    'Spirit Temple': {
        (6, 0, 0, 0): 84, # Armos
        (6, 0, 0, 1): 84, # Armos
        (6, 0, 0, 2): 138, # Beamos
        (6, 1, 0, 0): 84, # Armos
        (6, 1, 0, 1): 19, # Keese
        (6, 1, 0, 2): 19, # Keese
        (6, 1, 0, 3): 19, # Keese
        (6, 1, 0, 4): 19, # Keese
        (6, 2, 0, 0): EnemyLocation(19, [LOCATION_RESTRICTION.FLOATING], [], skip_raycast=True), # Keese
        (6, 2, 0, 1): EnemyLocation(19, [LOCATION_RESTRICTION.FLOATING], [], skip_raycast=True), # Keese
        (6, 2, 0, 2): EnemyLocation(19, [LOCATION_RESTRICTION.FLOATING], [], skip_raycast=True), # Keese
        (6, 2, 0, 3): EnemyLocation(19, [LOCATION_RESTRICTION.FLOATING], [], skip_raycast=True), # Keese
        (6, 2, 0, 5): 19, # Keese
        (6, 2, 0, 6): 17, # Wallmaster
        (6, 3, 0, 0): EnemyLocation(105, [LOCATION_RESTRICTION.FLOATING], [], skip_raycast=True), # Bubble
        (6, 3, 0, 3): 2, # Stalfos
        (6, 4, 0, 0): 149, # Skullwaltula
        (6, 4, 0, 1): 149, # Skullwaltula
        (6, 4, 0, 2): 149, # Skullwaltula
        (6, 4, 0, 3): 149, # Skullwaltula
        (6, 4, 0, 4): 37, # Lizalfos/Dinalfos
        (6, 4, 0, 5): 37, # Lizalfos/Dinalfos
        (6, 5, 0, 11): 84, # Armos
        (6, 8, 0, 4): 138, # Beamos
        (6, 8, 0, 5): 138, # Beamos
        (6, 8, 0, 6): 138, # Beamos
        (6, 10, 0, 0): 275, # Iron Knuckle
        (6, 12, 0, 0): 221, # Like like
        (6, 14, 0, 0): 431, # Wolfos
        (6, 15, 0, 8): 17, # Wallmaster
        (6, 15, 0, 9): 142, # Floormaster
        (6, 15, 0, 12): 221, # Like like
        (6, 16, 0, 0): 138, # Beamos
        (6, 17, 0, 0): EnemyLocation(246), # Anubis Spawner
        (6, 17, 0, 1): EnemyLocation(246), # Anubis Spawner
        (6, 17, 0, 2): EnemyLocation(246), # Anubis Spawner
        (6, 17, 0, 3): 138, # Beamos
        (6, 18, 0, 0): 84, # Armos
        (6, 18, 0, 1): 84, # Armos
        (6, 18, 0, 2): 84, # Armos
        #(6, 18, 0, 3): 84, # Armos # Leave one armos so we can press the switch
        (6, 20, 0, 0): 275, # Iron Knuckle
        (6, 22, 0, 10): 56, # Torch Slug
        (6, 22, 0, 11): 56, # Torch Slug
        (6, 22, 0, 12): 56, # Torch Slug
        (6, 22, 0, 13): 56, # Torch Slug
        (6, 23, 0, 1): 149, # Skullwaltula
        (6, 23, 0, 4): 138, # Beamos
        (6, 23, 0, 5): 138, # Beamos
        (6, 23, 0, 6): 138, # Beamos
        (6, 23, 0, 7): 138, # Beamos
        (6, 26, 0, 0): 105, # Bubble
        (6, 26, 0, 1): 105, # Bubble
        (6, 26, 0, 2): 105, # Bubble
        (6, 26, 0, 3): 37, # Lizalfos/Dinalfos
        (6, 26, 0, 4): 37, # Lizalfos/Dinalfos
        (6, 27, 0, 0): 246, # Anubis Spawner
    },
    'Shadow Temple': {
        (7, 1, 0, 0): 19, # Keese
        (7, 1, 0, 1): 19, # Keese
        (7, 1, 0, 2): 144, # Redead/Gibdo
        (7, 2, 0, 0): 138, # Beamos
        (7, 5, 0, 0): 138, # Beamos
        (7, 7, 0, 0): 144, # Redead/Gibdo
        (7, 7, 0, 1): 144, # Redead/Gibdo
        (7, 8, 0, 0): 55, # Skulltula
        (7, 8, 0, 1): 55, # Skulltula
        (7, 8, 0, 2): 55, # Skulltula
        (7, 8, 0, 3): 55, # Skulltula
        (7, 9, 0, 1): 105, # Bubble
        (7, 9, 0, 2): 17, # Wallmaster
        (7, 9, 0, 5): 138, # Beamos
        (7, 9, 0, 12): 2, # Stalfos
        (7, 11, 0, 0): 144, # Redead/Gibdo
        (7, 11, 0, 1): 144, # Redead/Gibdo
        (7, 13, 0, 0): 144, # Redead/Gibdo
        (7, 13, 0, 1): 144, # Redead/Gibdo
        (7, 14, 0, 0): 19, # Keese
        (7, 14, 0, 1): 19, # Keese
        (7, 14, 0, 2): 19, # Keese
        (7, 14, 0, 3): 19, # Keese
        (7, 15, 0, 0): 142, # Floormaster
        (7, 15, 0, 1): 142, # Floormaster
        (7, 16, 0, 0): 19, # Keese
        (7, 16, 0, 1): 19, # Keese
        (7, 16, 0, 2): 19, # Keese
        (7, 16, 0, 3): 221, # Like like
        (7, 17, 0, 0): 142, # Floormaster
        (7, 18, 0, 0): 55, # Skulltula
        (7, 19, 0, 0): 144, # Redead/Gibdo
        (7, 19, 0, 1): 144, # Redead/Gibdo
        (7, 20, 0, 0): 144, # Redead/Gibdo
        (7, 20, 0, 1): 144, # Redead/Gibdo
        (7, 21, 0, 13): 2, # Stalfos
        (7, 21, 0, 14): 2, # Stalfos
    },
    'Bottom of the Well': {
        (8, 0, 0, 0): 55, # Skulltula
        (8, 0, 0, 1): 55, # Skulltula
        (8, 0, 0, 2): 55, # Skulltula
        (8, 0, 0, 3): 55, # Skulltula
        (8, 0, 0, 4): 17, # Wallmaster
        (8, 0, 0, 5): 221, # Like like
        (8, 0, 0, 33): 105, # Bubble
        (8, 1, 0, 13): 144, # Redead/Gibdo
        (8, 1, 0, 14): 144, # Redead/Gibdo
        (8, 2, 0, 0): 144, # Redead/Gibdo
        (8, 3, 0, 0): 19, # Keese
        (8, 3, 0, 1): 19, # Keese
        (8, 3, 0, 2): 19, # Keese
        (8, 3, 0, 4): 138, # Beamos
        (8, 5, 0, 0): 19, # Keese
        (8, 5, 0, 1): 19, # Keese
        (8, 5, 0, 2): 19, # Keese
        (8, 5, 0, 3): 19, # Keese
        (8, 6, 0, 0): 85, # Deku Baba
    },
    'Ice Cavern': {
        (9, 1, 0, 1): 289, # Freezard
        (9, 1, 0, 10): 289, # Freezard
        (9, 1, 0, 11): 289, # Freezard
        (9, 1, 0, 12): 289, # Freezard
        (9, 5, 0, 3): 19, # Keese
        (9, 5, 0, 4): 19, # Keese
        (9, 5, 0, 5): 19, # Keese
        (9, 6, 0, 17): 289, # Freezard
        (9, 6, 0, 18): 289, # Freezard
        (9, 7, 0, 0): 431, # Wolfos
        (9, 8, 0, 8): 289, # Freezard
        (9, 9, 0, 0): 19, # Keese
        (9, 9, 0, 1): 19, # Keese
        (9, 9, 0, 2): 19, # Keese
        (9, 9, 0, 4): 289, # Freezard
        (9, 9, 0, 13): 289, # Freezard
        (9, 9, 0, 14): 289, # Freezard
        (9, 11, 0, 0): 19, # Keese
        (9, 11, 0, 1): 19, # Keese
        (9, 11, 0, 2): 19, # Keese
    },
    'Ganons Castle': {

        (13, 0, 0, 0): 138, # Beamos
        (13, 0, 0, 1): 138, # Beamos
        (13, 2, 0, 0): 289, # Freezard
        (13, 2, 0, 1): 289, # Freezard
        (13, 3, 0, 6): 17, # Wallmaster
        (13, 5, 0, 0): 431, # Wolfos
        (13, 6, 0, 1): 138, # Beamos
        (13, 8, 0, 11): 17, # Wallmaster
        (13, 9, 0, 6): 19, # Keese
        (13, 9, 0, 7): 19, # Keese
        (13, 9, 0, 8): 19, # Keese
        (13, 9, 0, 9): 55, # Skulltula
        (13, 10, 0, 1): 17, # Wallmaster
        (13, 12, 0, 0): 105, # Bubble
        (13, 12, 0, 3): 221, # Like like
        (13, 14, 0, 3): 56, # Torch Slug
        (13, 14, 0, 4): 105, # Bubble
        (13, 14, 0, 5): 105, # Bubble
        (13, 14, 0, 6): 105, # Bubble
        (13, 14, 0, 7): 105, # Bubble
        (13, 17, 0, 10): 138, # Beamos
        (13, 18, 0, 6): 56, # Torch Slug
        (13, 18, 0, 7): 56, # Torch Slug
        (13, 18, 0, 18): 17, # Wallmaster
        (13, 18, 0, 20): 17, # Wallmaster
        (13, 18, 0, 22): 17, # Wallmaster
    },
    'Gerudo Training Ground': {
        (11, 1, 0, 0): 2, # Stalfos
        (11, 1, 0, 1): 2, # Stalfos
        (11, 2, 0, 4): 17, # Wallmaster
        (11, 2, 0, 5): 17, # Wallmaster
        (11, 3, 0, 1): 431, # Wolfos
        (11, 3, 0, 2): 431, # Wolfos
        (11, 3, 0, 4): 431, # Wolfos
        (11, 3, 0, 5): 431, # Wolfos
        (11, 5, 0, 1): 56, # Torch Slug
        (11, 5, 0, 2): 56, # Torch Slug
        (11, 5, 0, 3): 19, # Keese
        (11, 5, 0, 4): 19, # Keese
        (11, 6, 0, 2): EnemyLocation(105, [LOCATION_RESTRICTION.FLOATING], []), # Bubble
        (11, 6, 0, 3): EnemyLocation(105, [LOCATION_RESTRICTION.FLOATING], []), # Bubble
        (11, 7, 0, 0): 37, # Lizalfos/Dinalfos
        (11, 7, 0, 1): 37, # Lizalfos/Dinalfos
        (11, 7, 0, 13): 138, # Beamos
        (11, 9, 0, 4): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (11, 9, 0, 5): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (11, 9, 0, 6): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (11, 9, 0, 7): EnemyLocation(197, [LOCATION_RESTRICTION.UNDERWATER], []), # Shell Blade
        (11, 10, 0, 0): 221, # Like like
        (11, 10, 0, 1): 221, # Like like
        (11, 10, 0, 2): 221, # Like like
    },
}

mq_dungeon_enemies = {
    'Deku Tree': {
        (0, 0, 0, 0): 199, # Whithered Deku Baba
        (0, 0, 0, 1): 199, # Whithered Deku Baba
        (0, 0, 0, 2): 19, # Keese
        (0, 0, 0, 3): 19, # Keese
        (0, 0, 0, 4): 149, # Skullwaltula
        (0, 0, 0, 10): 85, # Deku Baba
        (0, 0, 0, 11): 85, # Deku Baba
        (0, 0, 0, 22): 43, # Gohma Larva
        (0, 0, 0, 23): 43, # Gohma Larva
        (0, 1, 0, 3): 85, # Deku Baba
        (0, 1, 0, 9): 43, # Gohma Larva
        (0, 1, 0, 10): 43, # Gohma Larva
        (0, 2, 0, 0): 149, # Skullwaltula
        (0, 2, 0, 1): 149, # Skullwaltula
        (0, 2, 0, 2): 55, # Skulltula
        (0, 2, 0, 13): 43, # Gohma Larva
        (0, 2, 0, 14): 43, # Gohma Larva
        (0, 3, 0, 0): 199, # Whithered Deku Baba
        (0, 3, 0, 6): 85, # Deku Baba
        (0, 3, 0, 7): 85, # Deku Baba
        (0, 3, 0, 8): 85, # Deku Baba
        (0, 4, 0, 4): 96, # Deku Scrub
        (0, 4, 0, 5): 43, # Gohma Larva
        (0, 4, 0, 6): 43, # Gohma Larva
        (0, 4, 0, 7): 43, # Gohma Larva
        (0, 5, 0, 0): 199, # Whithered Deku Baba
        (0, 5, 0, 1): 55, # Skulltula
        (0, 5, 0, 7): 43, # Gohma Larva
        (0, 6, 0, 0): 19, # Keese
        (0, 6, 0, 3): 96, # Deku Scrub
        (0, 6, 0, 4): 43, # Gohma Larva
        (0, 6, 0, 5): 43, # Gohma Larva
        (0, 6, 0, 6): 43, # Gohma Larva
        (0, 6, 0, 7): 43, # Gohma Larva
        (0, 6, 0, 8): 43, # Gohma Larva
        (0, 6, 0, 9): 43, # Gohma Larva
        (0, 6, 0, 10): 43, # Gohma Larva
        (0, 6, 0, 11): 43, # Gohma Larva
        (0, 7, 0, 0): 199, # Whithered Deku Baba
        (0, 7, 0, 1): 19, # Keese
        (0, 7, 0, 2): 19, # Keese
        (0, 7, 0, 3): 19, # Keese
        (0, 7, 0, 4): 19, # Keese
        (0, 7, 0, 6): 85, # Deku Baba
        (0, 7, 0, 7): 85, # Deku Baba
        (0, 8, 0, 2): 85, # Deku Baba
        (0, 8, 0, 7): 43, # Gohma Larva
        (0, 8, 0, 8): 43, # Gohma Larva
        (0, 8, 0, 9): 43, # Gohma Larva
        (0, 8, 0, 10): 43, # Gohma Larva
        (0, 10, 0, 4): 85, # Deku Baba
        (0, 10, 0, 6): 43, # Gohma Larva
        (0, 10, 0, 7): 43, # Gohma Larva
        (0, 10, 0, 8): 43, # Gohma Larva
        (0, 10, 0, 9): 43, # Gohma Larva
        (0, 10, 0, 10): 43, # Gohma Larva
        (0, 10, 0, 11): 43, # Gohma Larva
    },
    'Dodongos Cavern': {
        (1, 1, 0, 2): 55, # Skulltula
        (1, 1, 0, 4): 19, # Keese
        (1, 1, 0, 5): 47, # Baby Dodongo
        (1, 1, 0, 6): 47, # Baby Dodongo
        (1, 2, 0, 1): 199, # Whithered Deku Baba
        (1, 2, 0, 2): 55, # Skulltula
        (1, 2, 0, 3): 55, # Skulltula
        (1, 2, 0, 7): 138, # Beamos
        (1, 2, 0, 8): 138, # Beamos
        (1, 3, 0, 1): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 2): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 3): 37, # Lizalfos/Dinalfos
        (1, 3, 0, 4): 37, # Lizalfos/Dinalfos
        (1, 5, 0, 4): 18, # Dodongo
        (1, 5, 0, 5): 18, # Dodongo
        (1, 5, 0, 6): 18, # Dodongo
        (1, 6, 0, 1): 43, # Gohma Larva
        (1, 6, 0, 2): 43, # Gohma Larva
        (1, 6, 0, 3): 43, # Gohma Larva
        (1, 6, 0, 4): 43, # Gohma Larva
        (1, 6, 0, 5): 43, # Gohma Larva
        (1, 7, 0, 0): 47, # Baby Dodongo
        (1, 7, 0, 1): 47, # Baby Dodongo
        (1, 8, 0, 0): 84, # Armos
        (1, 8, 0, 1): 84, # Armos
        (1, 8, 0, 2): 84, # Armos
        (1, 8, 0, 3): 84, # Armos
        (1, 8, 0, 4): 84, # Armos
        (1, 8, 0, 5): 84, # Armos
        (1, 8, 0, 6): 84, # Armos
        (1, 8, 0, 13): 47, # Baby Dodongo
        (1, 8, 0, 14): 47, # Baby Dodongo
        (1, 8, 0, 15): 37, # Lizalfos/Dinalfos
        (1, 10, 0, 0): 19, # Keese
        (1, 10, 0, 1): 19, # Keese
        (1, 10, 0, 2): 19, # Keese
        (1, 10, 0, 3): 55, # Skulltula
        (1, 10, 0, 4): 55, # Skulltula
        (1, 10, 0, 5): 55, # Skulltula
        (1, 10, 0, 8): 47, # Baby Dodongo
        (1, 10, 0, 9): 47, # Baby Dodongo
        (1, 10, 0, 10): 47, # Baby Dodongo
        (1, 12, 0, 0): 19, # Keese
        (1, 12, 0, 1): 19, # Keese
        (1, 13, 0, 2): 96, # Deku Scrub
        (1, 13, 0, 3): 96, # Deku Scrub
        (1, 13, 0, 4): 19, # Keese
        (1, 15, 0, 0): 149, # Skullwaltula
        (1, 15, 0, 1): 55, # Skulltula
        (1, 15, 0, 2): 55, # Skulltula
        (1, 15, 0, 3): 55, # Skulltula
    },
    'Jabu Jabus Belly': {
        (2, 0, 0, 0): 14, # Octorok
    (2, 0, 0, 7): 45, # Shabom
    (2, 0, 0, 8): 45, # Shabom
    (2, 0, 0, 9): 45, # Shabom
    (2, 1, 0, 3): 52, # Biri
    (2, 1, 0, 4): 52, # Biri
    (2, 1, 0, 16): 396, # Stinger
    (2, 2, 0, 2): 52, # Biri
    (2, 2, 0, 3): 52, # Biri
    (2, 3, 0, 3): 52, # Biri
    (2, 3, 0, 10): 45, # Shabom
    (2, 4, 0, 7): 37, # Lizalfos/Dinalfos
    (2, 5, 0, 4): 221, # Like like
    (2, 5, 0, 5): 221, # Like like
    (2, 6, 0, 0): 99, # Bari
    (2, 7, 0, 0): 37, # Lizalfos/Dinalfos
    (2, 11, 0, 5): EnemyLocation(221, patch_func=patch_mq_jabu_likelike_right), # Like like
    (2, 11, 0, 6): EnemyLocation(221, patch_func=patch_mq_jabu_likelike_left), # Like like
    (2, 12, 0, 0): 149, # Skullwaltula
    (2, 12, 0, 1): 53, # Tailpasaran
    (2, 12, 0, 2): 53, # Tailpasaran
    (2, 12, 0, 3): 53, # Tailpasaran
    (2, 12, 0, 9): 45, # Shabom
    (2, 12, 0, 10): 45, # Shabom
    (2, 13, 0, 1): 19, # Keese
    (2, 13, 0, 2): 19, # Keese
    (2, 13, 0, 3): 19, # Keese
    (2, 13, 0, 5): 396, # Stinger
    (2, 13, 0, 6): 396, # Stinger
    (2, 14, 0, 0): 58, # Singray
    (2, 14, 0, 1): 58, # Singray
    (2, 14, 0, 3): 221, # Like like
    (2, 14, 0, 4): 37, # Lizalfos/Dinalfos
    },
    'Forest Temple': {
        (3, 0, 0, 0): 149, # Skullwaltula
    (3, 0, 0, 1): 149, # Skullwaltula
    (3, 0, 0, 2): 149, # Skullwaltula
    (3, 0, 0, 3): 149, # Skullwaltula
    (3, 0, 0, 4): 149, # Skullwaltula
    (3, 0, 0, 5): 55, # Skulltula
    (3, 1, 0, 0): 55, # Skulltula
    (3, 1, 0, 1): 55, # Skulltula
    (3, 1, 0, 2): 55, # Skulltula
    (3, 5, 0, 4): 2, # Stalfos
    (3, 6, 0, 0): 431, # Wolfos
    (3, 6, 0, 1): 431, # Wolfos
    (3, 7, 0, 2): 149, # Skullwaltula
    (3, 7, 0, 3): 85, # Deku Baba
    (3, 7, 0, 4): 85, # Deku Baba
    (3, 7, 0, 5): 85, # Deku Baba
    (3, 8, 0, 0): 14, # Octorok
    (3, 8, 0, 1): 14, # Octorok
    (3, 8, 0, 2): 14, # Octorok
    (3, 8, 0, 3): 149, # Skullwaltula
    (3, 8, 0, 4): 149, # Skullwaltula
    (3, 8, 0, 5): 149, # Skullwaltula
    (3, 8, 0, 6): 55, # Skulltula
    (3, 10, 0, 0): 55, # Skulltula
    (3, 11, 0, 1): 105, # Bubble
    (3, 11, 0, 2): 105, # Bubble
    (3, 15, 0, 0): 55, # Skulltula
    (3, 15, 0, 1): 55, # Skulltula
    (3, 15, 0, 2): 55, # Skulltula
    (3, 15, 0, 3): 55, # Skulltula
    (3, 15, 0, 4): 55, # Skulltula
    (3, 15, 0, 5): 55, # Skulltula
    (3, 15, 0, 6): 55, # Skulltula
    (3, 17, 0, 0): 55, # Skulltula
    (3, 17, 0, 1): 55, # Skulltula
    (3, 18, 0, 0): 144, # Redead/Gibdo
    (3, 19, 0, 0): EnemyLocation(17, skip_raycast=True), # Wallmaster
    (3, 20, 0, 0): EnemyLocation(105, skip_raycast=True), # Bubble
    (3, 20, 0, 1): EnemyLocation(105, skip_raycast=True), # Bubble
    (3, 20, 0, 2): 17, # Wallmaster
    (3, 21, 0, 0): 142, # Floormaster
    },
    'Fire Temple': {
        (4, 3, 0, 0): 153, # Flare Dancer
    (4, 4, 0, 3): 37, # Lizalfos/Dinalfos
    (4, 5, 0, 6): 149, # Skullwaltula
    (4, 5, 0, 8): 37, # Lizalfos/Dinalfos
    (4, 5, 0, 9): 37, # Lizalfos/Dinalfos
    (4, 5, 0, 10): 37, # Lizalfos/Dinalfos
    (4, 5, 0, 11): 37, # Lizalfos/Dinalfos
    (4, 7, 0, 2): 56, # Torch Slug
    (4, 7, 0, 3): 56, # Torch Slug
    (4, 14, 0, 2): 2, # Stalfos
    (4, 14, 0, 3): 2, # Stalfos
    (4, 15, 0, 0): 19, # Keese
    (4, 15, 0, 2): 2, # Stalfos
    (4, 15, 0, 3): 2, # Stalfos
    (4, 17, 0, 2): 221, # Like like
    (4, 18, 0, 0): 275, # Iron Knuckle
    (4, 24, 0, 0): 153, # Flare Dancer
    (4, 25, 0, 0): 37, # Lizalfos/Dinalfos
    },
    'Water Temple': {
        (5, 2, 0, 1): 236, # Spike
    (5, 3, 0, 5): 2, # Stalfos
    (5, 3, 0, 6): 2, # Stalfos
    (5, 6, 0, 2): 2, # Stalfos
    (5, 6, 0, 3): 2, # Stalfos
    (5, 6, 0, 4): 2, # Stalfos
    (5, 10, 0, 0): 37, # Lizalfos/Dinalfos
    (5, 14, 0, 1): 18, # Dodongo
    (5, 14, 0, 2): 18, # Dodongo
    (5, 14, 0, 3): 18, # Dodongo
    (5, 14, 0, 4): 18, # Dodongo
    (5, 14, 0, 5): 18, # Dodongo
    (5, 14, 0, 6): 18, # Dodongo
    (5, 14, 0, 7): 18, # Dodongo
    (5, 16, 0, 1): 2, # Stalfos
    (5, 18, 0, 0): 236, # Spike
    (5, 18, 0, 1): 37, # Lizalfos/Dinalfos
    (5, 18, 0, 2): 37, # Lizalfos/Dinalfos
    (5, 19, 0, 0): 2, # Stalfos
    (5, 19, 0, 1): 2, # Stalfos
    (5, 19, 0, 2): 2, # Stalfos
    (5, 20, 0, 0): 37, # Lizalfos/Dinalfos
    (5, 20, 0, 1): 37, # Lizalfos/Dinalfos
    },
    'Spirit Temple': {
        (6, 1, 0, 0): 56, # Torch Slug
    (6, 1, 0, 1): 56, # Torch Slug
    (6, 1, 0, 2): 19, # Keese
    (6, 1, 0, 3): 19, # Keese
    (6, 2, 0, 0): 144, # Redead/Gibdo
    (6, 2, 0, 1): 144, # Redead/Gibdo
    (6, 2, 0, 2): 144, # Redead/Gibdo
    (6, 3, 0, 0): EnemyLocation(19, restrictions=[LOCATION_RESTRICTION.FLOATING], skip_raycast=True), # Keese
    (6, 3, 0, 1): EnemyLocation(19, restrictions=[LOCATION_RESTRICTION.FLOATING], skip_raycast=True), # Keese
    (6, 3, 0, 2): EnemyLocation(19, restrictions=[LOCATION_RESTRICTION.FLOATING], skip_raycast=True), # Keese
    (6, 3, 0, 3): EnemyLocation(19, restrictions=[LOCATION_RESTRICTION.FLOATING], skip_raycast=True), # Keese
    (6, 3, 0, 4): EnemyLocation(19, restrictions=[LOCATION_RESTRICTION.FLOATING], skip_raycast=True), # Keese
    (6, 3, 0, 12): 246, # Anubis Spawner
    (6, 4, 0, 0): 47, # Baby Dodongo
    (6, 4, 0, 1): 47, # Baby Dodongo
    (6, 4, 0, 2): 47, # Baby Dodongo
    (6, 4, 0, 3): 47, # Baby Dodongo
    (6, 4, 0, 4): 221, # Like like
    (6, 4, 0, 11): 138, # Beamos
    (6, 5, 0, 0): 17, # Wallmaster
    (6, 5, 0, 1): 142, # Floormaster
    (6, 5, 0, 20): 17, # Wallmaster
    (6, 8, 0, 2): 105, # Bubble
    (6, 8, 0, 3): 105, # Bubble
    (6, 8, 0, 4): 105, # Bubble
    (6, 8, 0, 18): 17, # Wallmaster
    (6, 8, 0, 20): 17, # Wallmaster
    (6, 9, 0, 0): 55, # Skulltula
    (6, 10, 0, 5): 275, # Iron Knuckle
    (6, 12, 0, 0): 55, # Skulltula
    (6, 12, 0, 1): 55, # Skulltula
    (6, 12, 0, 2): 55, # Skulltula
    (6, 12, 0, 3): 55, # Skulltula
    (6, 12, 0, 4): 55, # Skulltula
    (6, 12, 0, 5): 55, # Skulltula
    (6, 12, 0, 6): 55, # Skulltula
    (6, 12, 0, 7): 55, # Skulltula
    (6, 12, 0, 8): 55, # Skulltula
    (6, 13, 0, 1): 75, # Moblin
    (6, 15, 0, 0): 2, # Stalfos
    (6, 15, 0, 1): 2, # Stalfos
    (6, 15, 0, 2): 17, # Wallmaster
    (6, 15, 0, 7): 17, # Wallmaster
    (6, 15, 0, 9): 17, # Wallmaster
    (6, 15, 0, 11): 17, # Wallmaster
    (6, 17, 0, 6): 138, # Beamos
    (6, 17, 0, 7): 138, # Beamos
    (6, 17, 0, 8): 138, # Beamos
    (6, 17, 0, 9): 138, # Beamos
    (6, 18, 0, 0): 37, # Lizalfos/Dinalfos
    (6, 18, 0, 1): 37, # Lizalfos/Dinalfos
    (6, 19, 0, 0): 142, # Floormaster
    (6, 20, 0, 5): 275, # Iron Knuckle
    (6, 21, 0, 0): 144, # Redead/Gibdo
    (6, 22, 0, 0): 275, # Iron Knuckle
    (6, 23, 0, 0): 149, # Skullwaltula
    (6, 23, 0, 1): 56, # Torch Slug
    (6, 23, 0, 2): 19, # Keese
    (6, 23, 0, 3): 19, # Keese
    (6, 23, 0, 4): 19, # Keese
    (6, 23, 0, 5): 19, # Keese
    (6, 26, 0, 0): 56, # Torch Slug
    (6, 26, 0, 1): 37, # Lizalfos/Dinalfos
    (6, 26, 0, 6): 105, # Bubble
    (6, 26, 0, 7): 105, # Bubble
    (6, 27, 0, 7): EnemyLocation(2, skip_raycast=True, patch_func=patch_mq_spirit_child_stalfos), # Stalfos
    },
    'Shadow Temple': {
(7, 1, 0, 0): 144, # Redead/Gibdo
    (7, 1, 0, 1): 144, # Redead/Gibdo
    (7, 1, 0, 2): 144, # Redead/Gibdo
    (7, 1, 0, 3): 144, # Redead/Gibdo
    (7, 5, 0, 0): 138, # Beamos
    (7, 6, 0, 0): 55, # Skulltula
    (7, 6, 0, 1): 55, # Skulltula
    (7, 6, 0, 2): 55, # Skulltula
    (7, 6, 0, 3): 55, # Skulltula
    (7, 7, 0, 0): 144, # Redead/Gibdo
    (7, 7, 0, 1): 144, # Redead/Gibdo
    (7, 8, 0, 1): 55, # Skulltula
    (7, 8, 0, 2): 138, # Beamos
    (7, 8, 0, 3): 138, # Beamos
    (7, 9, 0, 5): 105, # Bubble
    (7, 9, 0, 6): 138, # Beamos
    (7, 9, 0, 7): 138, # Beamos
    (7, 9, 0, 10): 138, # Beamos
    (7, 11, 0, 8): 144, # Redead/Gibdo
    (7, 11, 0, 9): 144, # Redead/Gibdo
    (7, 13, 0, 0): 19, # Keese
    (7, 13, 0, 1): 19, # Keese
    (7, 13, 0, 2): 19, # Keese
    (7, 13, 0, 3): 19, # Keese
    (7, 13, 0, 4): 55, # Skulltula
    (7, 13, 0, 5): 55, # Skulltula
    (7, 13, 0, 6): 55, # Skulltula
    (7, 13, 0, 7): 55, # Skulltula
    (7, 14, 0, 4): 2, # Stalfos
    (7, 14, 0, 5): 2, # Stalfos
    (7, 15, 0, 0): 105, # Bubble
    (7, 15, 0, 1): 105, # Bubble
    (7, 15, 0, 2): 221, # Like like
    (7, 16, 0, 0): 19, # Keese
    (7, 16, 0, 1): 19, # Keese
    (7, 16, 0, 2): 19, # Keese
    (7, 16, 0, 3): 221, # Like like
    (7, 18, 0, 0): 55, # Skulltula
    (7, 19, 0, 0): 144, # Redead/Gibdo
    (7, 19, 0, 1): 144, # Redead/Gibdo
    (7, 19, 0, 2): 144, # Redead/Gibdo
    (7, 19, 0, 3): 144, # Redead/Gibdo
    (7, 20, 0, 0): 144, # Redead/Gibdo
    (7, 20, 0, 1): 144, # Redead/Gibdo
    (7, 21, 0, 3): 149, # Skullwaltula
    (7, 21, 0, 4): 55, # Skulltula
    (7, 21, 0, 16): 2, # Stalfos
    (7, 21, 0, 17): 2, # Stalfos
    },
    'Bottom of the Well': {
        (8, 0, 0, 0): 149, # Skullwaltula
    (8, 0, 0, 1): 149, # Skullwaltula
    (8, 0, 0, 2): 55, # Skulltula
    (8, 0, 0, 3): 17, # Wallmaster
    (8, 0, 0, 4): 144, # Redead/Gibdo
    (8, 1, 0, 1): 55, # Skulltula
    (8, 1, 0, 2): 55, # Skulltula
    (8, 1, 0, 3): 55, # Skulltula
    (8, 1, 0, 4): 17, # Wallmaster
    (8, 1, 0, 5): 144, # Redead/Gibdo
    (8, 1, 0, 6): 144, # Redead/Gibdo
    (8, 1, 0, 7): 144, # Redead/Gibdo
    (8, 1, 0, 8): 144, # Redead/Gibdo
    (8, 1, 0, 9): 144, # Redead/Gibdo
    (8, 2, 0, 0): 144, # Redead/Gibdo
    (8, 3, 0, 0): 17, # Wallmaster
    (8, 3, 0, 1): 142, # Floormaster
    (8, 6, 0, 0): 19, # Keese
    (8, 6, 0, 1): 19, # Keese
    (8, 6, 0, 2): 19, # Keese
    (8, 6, 0, 3): 55, # Skulltula
    (8, 6, 0, 4): 55, # Skulltula
    },
    'Ice Cavern': {
        (9, 1, 0, 0): 289, # Freezard
    (9, 1, 0, 1): 27, # Tektite
    (9, 1, 0, 2): 27, # Tektite
    (9, 3, 0, 5): 431, # Wolfos
    (9, 3, 0, 6): 289, # Freezard
    (9, 3, 0, 7): 289, # Freezard
    (9, 5, 0, 3): 431, # Wolfos
    (9, 5, 0, 4): 431, # Wolfos
    (9, 5, 0, 5): 19, # Keese
    (9, 5, 0, 6): 19, # Keese
    (9, 6, 0, 3): 19, # Keese
    (9, 6, 0, 4): 19, # Keese
    (9, 7, 0, 3): 2, # Stalfos
    (9, 8, 0, 0): 289, # Freezard
    (9, 8, 0, 1): 289, # Freezard
    (9, 9, 0, 0): 289, # Freezard
    (9, 9, 0, 1): 289, # Freezard
    (9, 9, 0, 5): 289, # Freezard
    (9, 11, 0, 11): 431, # Wolfos
    (9, 11, 0, 12): 431, # Wolfos
    (9, 11, 0, 13): 149, # Skullwaltula
    },
    'Gerudo Training Ground': {
        (11, 1, 0, 0): 275, # Iron Knuckle
    (11, 2, 0, 0): 289, # Freezard
    (11, 2, 0, 17): 17, # Wallmaster
    (11, 2, 0, 21): 17, # Wallmaster
    (11, 3, 0, 4): 2, # Stalfos
    (11, 3, 0, 5): 2, # Stalfos
    (11, 3, 0, 6): 55, # Skulltula
    (11, 3, 0, 7): 55, # Skulltula
    (11, 3, 0, 8): 55, # Skulltula
    (11, 5, 0, 0): 275, # Iron Knuckle
    (11, 5, 0, 1): 56, # Torch Slug
    (11, 5, 0, 2): 56, # Torch Slug
    (11, 6, 0, 1): 105, # Bubble
    (11, 6, 0, 2): 105, # Bubble
    (11, 6, 0, 3): 105, # Bubble
    (11, 7, 0, 0): 37, # Lizalfos/Dinalfos
    (11, 7, 0, 1): 37, # Lizalfos/Dinalfos
    (11, 7, 0, 2): 37, # Lizalfos/Dinalfos
    (11, 7, 0, 3): 18, # Dodongo
    (11, 7, 0, 4): 18, # Dodongo
    (11, 7, 0, 5): 84, # Armos
    (11, 9, 0, 0): 396, # Stinger
    (11, 9, 0, 1): 396, # Stinger
    (11, 9, 0, 3): 99, # Bari
    (11, 9, 0, 4): 197, # Shell Blade
    (11, 10, 0, 0): 289, # Freezard
    (11, 10, 0, 1): 289, # Freezard
    (11, 10, 0, 2): 236, # Spike
    (11, 10, 0, 3): 236, # Spike
    (11, 10, 0, 4): 236, # Spike
    },
    'Ganons Castle': {
        (13, 0, 0, 0): 84, # Armos
    (13, 0, 0, 1): 84, # Armos
    (13, 0, 0, 2): 275, # Iron Knuckle
    (13, 0, 0, 9): 105, # Bubble
    (13, 0, 0, 10): 105, # Bubble
    (13, 2, 0, 1): 289, # Freezard
    (13, 2, 0, 2): 289, # Freezard
    (13, 2, 0, 3): 289, # Freezard
    (13, 3, 0, 0): 19, # Keese
    (13, 3, 0, 3): 19, # Keese
    (13, 3, 0, 4): 19, # Keese
    (13, 3, 0, 5): 19, # Keese
    (13, 5, 0, 1): 2, # Stalfos
    (13, 5, 0, 2): 2, # Stalfos
    (13, 6, 0, 1): 84, # Armos
    (13, 6, 0, 8): 138, # Beamos
    (13, 6, 0, 9): 138, # Beamos
    (13, 6, 0, 10): 138, # Beamos
    (13, 6, 0, 11): 138, # Beamos
    (13, 6, 0, 12): 138, # Beamos
    (13, 6, 0, 13): 138, # Beamos
    (13, 8, 0, 3): 138, # Beamos
    (13, 9, 0, 6): 56, # Torch Slug
    (13, 9, 0, 7): 56, # Torch Slug
    (13, 9, 0, 8): 37, # Lizalfos/Dinalfos
    (13, 10, 0, 3): 149, # Skullwaltula
    (13, 12, 0, 5): 105, # Bubble
    (13, 12, 0, 6): 138, # Beamos
    (13, 12, 0, 7): 138, # Beamos
    (13, 12, 0, 8): 138, # Beamos
    (13, 12, 0, 9): 138, # Beamos
    (13, 14, 0, 1): 56, # Torch Slug
    (13, 14, 0, 2): 56, # Torch Slug
    (13, 14, 0, 16): 138, # Beamos
    (13, 17, 0, 9): 56, # Torch Slug
    (13, 17, 0, 10): 19, # Keese
    (13, 17, 0, 11): 19, # Keese
    (13, 17, 0, 12): 275, # Iron Knuckle
    (13, 18, 0, 6): 144, # Redead/Gibdo
    (13, 18, 0, 7): 144, # Redead/Gibdo
    (13, 18, 0, 8): 144, # Redead/Gibdo
    (13, 18, 0, 9): 105, # Bubble
    (13, 18, 0, 10): 105, # Bubble
    (13, 18, 0, 24): 17, # Wallmaster
    }
}

named_rooms: dict[str, tuple[int,int]] = {
    'KAK REDEAD GROTTO': (0x3E, 2),
    'ROYAL FAMILY TOMB ENTRYWAY': (0x41,0),
    'SFM WOLFOS GROTTO': (0x3E, 7),
    'JABU COMPASS': (2, 12),
    'FOREST TEMPLE LOWER STALFOS': (3,6),
    'FOREST TEMPLE BEFORE LEDGE': (3, 21),
    'FIRE TEMPLE LOWER LOCKED DOOR': (4,15),
    'WATER TEMPLE MAP CHEST': (5, 19),
    'WATER TEMPLE TORCHES CHEST': (5,18),
    'WATER TEMPLE CENTRAL PILLAR': (5,2),
    'SPIRIT TEMPLE CHILD START': (6,1),
    'SPIRIT TEMPLE ADULT ANUBIS ROOM': (6,17),
    'SHADOW TEMPLE MAP CHEST': (7,1),
    'SHADOW TEMPLE COMPASS CHEST': (7,7),
    'SHADOW TEMPLE INVISIBLE BLADES': (7,16),
    'SHADOW TEMPLE INVISIBLE SPIKES': (7,11),
    'SHADOW TEMPLE AFTER WIND': (7,20),
    'ICE CAVERN ENTRYWAY': (9,1),
    'GANONS TOWER LIZALFOS': (10,0),
    'GANONS TOWER STALFOS': (10,2),
    'GANONS TOWER KNUCKLES': (10,4),
    'GTG STALFOS ROOM': (11,1),
    'GTG BEAMOS ROOM': (11,7),
    'GTG BEFORE HEAVY BLOCK': (11,3),
    'GTG HEAVY BLOCK': (11,10),
    'GTG HAMMER ROOM': (11,5),
    'GANONS CASTLE WATER TRIAL ENTRY': (13,2),
    'GANONS CASTLE LIGHT TRIAL INVISIBLE ENEMIES': (13,9),
}

class Enemy:
    def __init__(self, name: str, id:int, var: int = 0, weight=1, filter_func = None, kill_logic: str = 'worst_case_kill_logic', drop_logic = None, soul_name = None, meets_location_restrictions: list[int] = [], required_categories: list[int] = []):
        self.name = name
        self.id = id
        self.var = var
        self.filter_func = filter_func
        self.kill_logic = kill_logic
        self.meets_location_restrictions = meets_location_restrictions
        self.required_categories = required_categories
        self.weight = weight
        self.drop_logic = drop_logic if drop_logic is not None else self.kill_logic
        if soul_name:
            self.soul_name = soul_name
        else:
            self.soul_name = self.name

# Filter functions, return false to filter out enemy from being shuffled

def filter_skullwalltula(actor: Actor):
    # Filter gold skulltulas, type == 4 or type == 5
    type = (actor.var & 0xE000) >> 13
    return not (type == 4 or type == 5)

def filter_armos(actor: Actor):
    # Filter armos, var == 0 is a pushable statue so we don't want to filter these
    return actor.var != 0

def filter_skullkids(actor: Actor):
    # Filter skull kids, type <= 6 are the ocarina game ones
    type = (actor.var >> 0x0A) & 0x3F
    return type > 6

enemy_filters = {
    0x0054: filter_armos,
    0x0095: filter_skullwalltula,
    0x0115: filter_skullkids
}

enemy_actor_types: list[Enemy] = {
    Enemy("Stalfos", id=0x0002, var=0x0003, kill_logic='can_kill_stalfos', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Octorok", id=0x000E, kill_logic='can_kill_octorok', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_WATER], required_categories=[ENEMY_RESTRICTION.ABOVE_WATER]),
    Enemy("Wallmaster", id=0x0011, kill_logic='can_kill_wallmaster', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Dodongo", id=0x0012, kill_logic='can_kill_dodongo', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
        Enemy("Keese", id=0x0013, var=0x0002, kill_logic='can_kill_keese', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER]),
        Enemy("Fire Keese", id=0x0013, var=0x0000, kill_logic='can_kill_keese', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER], soul_name="Keese"),
        Enemy("Ice Keese", id=0x0013, var=0x0004, kill_logic='can_kill_keese', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER], soul_name="Keese"),
    Enemy("Tektite", id=0x001B, kill_logic='can_kill_tektite', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
        Enemy("Tektite (Blue)", id=0x001B, var=0xFFFE, kill_logic='can_kill_tektite', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER], soul_name="Tektite"),
    Enemy("Peahat", id=0x001D, var=0xFFFF, weight=.5, kill_logic='can_kill_peahat', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER]),
        Enemy("Flying Peahat", id=0x001D, var=0x0000, weight=.5, kill_logic='can_kill_flying_peahat', soul_name="Peahat", meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER], required_categories=[ENEMY_RESTRICTION.OUTSIDE]),
    Enemy("Lizalfos", id=0x0025, var=0xFF80, soul_name="Lizalfos and Dinalfos", kill_logic='can_kill_lizalfos', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
        Enemy("Dinalfos", id=0x0025, var=0xFFFE, soul_name="Lizalfos and Dinalfos", kill_logic='can_kill_lizalfos', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Gohma Larva", id=0x002B, var=0x0006, soul_name="Gohma Larvae", kill_logic='can_kill_gohma_larva', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Shabom", id=0x002D, kill_logic='can_kill_shabom', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER]),
    Enemy("Baby Dodongo", id=0x002F, kill_logic='can_kill_baby_dodongo'),
    Enemy("Biri", id=0x0034, soul_name="Biri and Bari", kill_logic='can_kill_biri', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER]),
    Enemy("Bari", id=0x0063, soul_name="Biri and Bari", kill_logic='can_kill_biri', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Tailpasaran", id=0x0035, var=0xFFFF, kill_logic='can_kill_tailsparan', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER]),
    Enemy("Skulltula", id=0x0037, kill_logic='can_kill_skulltula', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Torch Slug", kill_logic='can_kill_torch_slug', id=0x0038),
        Enemy("Moblin", kill_logic='can_kill_moblin', id=0x004B, var=0x0002, weight=.5, meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
        Enemy("Moblin (Spear)", kill_logic='can_kill_moblin', soul_name="Moblin", id=0x004B, var=0xFFFF, weight=.5, meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Armos", id=0x0054, var = 0xFFFF, kill_logic='can_kill_armos', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Deku Baba", id=0x0055, soul_name="Deku Baba", kill_logic='can_kill_deku_baba_enemizer', drop_logic='can_kill_deku_baba'),
    #Enemy("Whithered Deku Baba", id=0x00C7, soul_name="Deku Baba", kill_logic='can_kill_deku_baba_enemizer'),
    Enemy("Deku Scrub", id=0x0060, kill_logic='can_kill_scrub', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER]),
    Enemy("Bubble", id=0x0069, var=0xFFFF, kill_logic='can_kill_bubble'),
        Enemy("Beamos (Large)", id=0x008A, var=0x0500, kill_logic='can_kill_beamos', soul_name='Beamos'),
        Enemy("Beamos (Small)", id=0x008A, var=0x0501, kill_logic='can_kill_beamos', soul_name='Beamos'),
    Enemy("Floormaster", id=0x008E, kill_logic='can_kill_floormaster', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
        Enemy("Redead", id=0x0090, var=0x7F02, soul_name="Redead and Gibdo", kill_logic='can_kill_redead'),
        Enemy("Gibdo", id=0x0090, var=0x7FFE, soul_name="Redead and Gibdo", kill_logic='can_kill_redead', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Skullwalltula", id=0x0095, kill_logic='can_kill_skullwalltula', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING]),
    Enemy("Flare Dancer", id=0x0099, kill_logic='can_kill_flare_dancer', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Shell Blade", id=0x00C5, kill_logic='can_kill_shell_blade', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Like like", id=0x00DD, soul_name="Like-like", kill_logic='can_kill_likelike', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Spike Enemy", id=0x00EC, kill_logic='can_kill_spike_enemy', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Anubis Spawner", id=0x00F6, var=0x0003, soul_name="Anubis", kill_logic='can_kill_anubis', meets_location_restrictions=[LOCATION_RESTRICTION.FLOATING]),
        Enemy("Iron Knuckle (Black)", kill_logic='can_kill_iron_knuckle', id=0x0113, var=0xFF82, weight=.5, meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], soul_name='Iron Knuckle'),
        Enemy("Iron Knuckle (White)", kill_logic='can_kill_iron_knuckle', id=0x0113, var=0xFF83, weight=.5, meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND], soul_name='Iron Knuckle'),
    Enemy("Skull Kid", kill_logic='can_kill_skull_kid', id=0x0115, var=0xFFFF),
    Enemy("Freezard", kill_logic='can_kill_freezard', id=0x0121, meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Stinger", id=0x018C, kill_logic='can_kill_stinger', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER], required_categories=[ENEMY_RESTRICTION.ABOVE_WATER]),
    Enemy("Stingray", id=0x003A, var=0x000A, soul_name="Stinger", kill_logic='can_kill_stinger', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER]),
    Enemy("Wolfos", id=0x01AF, var=0xFF00, kill_logic='can_kill_wolfos', meets_location_restrictions=[LOCATION_RESTRICTION.ABOVE_GROUND]),
    Enemy("Guay", id=0x01C0, kill_logic='can_kill_basic', meets_location_restrictions=[LOCATION_RESTRICTION.UNDERWATER, LOCATION_RESTRICTION.FLOATING, LOCATION_RESTRICTION.ABOVE_GROUND, LOCATION_RESTRICTION.ABOVE_WATER]),
}

enemies_by_name = {enemy.name: enemy for enemy in enemy_actor_types}
