from dataclasses import dataclass
from typing import List


from lib.models.enums import Ability, ArmorType, WeaponType


@dataclass
class CharacterClass:
    name: str
    description: str
    hit_dice: str #TO-DO: Probably better to make this into a class at some point.
    primary_ability: Ability
    save_proficiency: List[Ability]
    armor_proficiency: List[ArmorType]
    weapon_proficiency: List[WeaponType]
