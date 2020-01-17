from dataclasses import dataclass
from typing import List, Dict

from lib.models.character_class import CharacterClass
from lib.models.entity import *
from lib.models.enums import Ability, Skill, Alignment


@dataclass
class Creature(Entity):
    name: str
    description: str
    character_class: CharacterClass 
    level: int
    background: str
    race: str
    alignment: Alignment
    xp: int
    abilities: Dict[Ability, int]
    skills: List[Skill]
    max_hp: int
    current_hp: int
    temporary_hp: int
    armor_class: int
    hd_value: int
    hd_total: int
    death_save_success: int = 0
    death_save_failure: int = 0
    inventory: Inventory = Inventory()

    def get_modifier(self, ability: Ability) -> int:
        value = self.abilities.get(ability)
        print(self.abilities)
        return (value - 10) // 2

    def get_initiative(self) -> int:
        raise NotImplementedError

    def get_passive_perception(self) -> int:
        raise NotImplementedError

    def take_damage(self, damage: int) -> int:
        self.current_hp -= damage
        return self.current_hp

    def heal(self, amount: int) -> int:
        self.current_hp += amount
        return self.current_hp
