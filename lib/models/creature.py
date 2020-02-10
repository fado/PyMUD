from dataclasses import dataclass, field
from typing import List, Dict

from dice import roll
from game_data import rooms
from lib.constants import DEFAULT_START_LOCATION
from lib.models.character_class import CharacterClass
from lib.models.entity import Entity, Inventory
from lib.models.enums import Ability, Skill, Alignment


class Creature(Entity):

    _DEFAULT_LEVEL = 0
    _DEFAULT_XP = 0
    _DEFAULT_HP = 1
    _DEFAULT_AC = 10

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 character_class: CharacterClass = None,
                 level: int = _DEFAULT_LEVEL,
                 background: str = None,
                 race: str = None,
                 alignment: Alignment = None,
                 xp: int = _DEFAULT_XP,
                 abilities: Dict[Ability, int] = None,
                 skills: List[Skill] = None,
                 max_hp: int = _DEFAULT_HP, 
                 armor_class: int = _DEFAULT_AC,
                 hd_value: int = 0,
                 hd_total: int = 0,
                 inventory: Inventory = None):

        self.character_class = character_class
        self.level = level
        self.background = background
        self.race = race
        self.alignment = alignment
        self.xp = xp
        self.abilities = abilities
        self.skills = skills
        self.max_hp = max_hp
        self.current_hp: int = self.max_hp
        self.temporary_hp: int = 0
        self.armor_class = armor_class
        self.hd_value = hd_value
        self.hd_total = hd_total
        self.death_save_success: int = 0
        self.death_save_failure: int = 0
        self.inventory: Inventory = inventory
        self.initiative = None
        self._location = ""
        self.target: Character = None #TODO Make this a list.
        self.dead: bool = False #TODO Appropriate wordage?

        super().__init__()

    def get_modifier(self, ability: Ability) -> int:
        value = self.abilities.get(ability)
        return (value - 10) // 2

    def get_strength_modifier(self) -> int:
        return self.get_modifier(Ability.STRENGTH)

    def get_dexterity_modifier(self) -> int:
        return self.get_modifier(Ability.DEXTERITY)

    def get_constitution_modifier(self) -> int:
        return self.get_modifier(Ability.CONSTITUTION)

    def get_wisdom_modifier(self) -> int:
        return self.get_modifier(Ability.WISDOM)

    def get_intelligence_modifier(self) -> int:
        return self.get_modifier(Ability.INTELLIGENCE)

    def get_charisma_modifier(self) -> int:
        return self.get_modifier(Ability.CHARISMA)

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

    def move(self, destination: str):
        self._location = destination
        rooms[self._location].inventory.add_item(self)

    # I don't mind people reading the location, but I want to discourage them from
    # setting it. They should use the above method.
    def get_location(self) -> str:
        return self._location

    # TO-DO: Eventually other things will need to be taken into consideration, but
    # we can worry about that down the road.
    def roll_initiative(self) -> int:
        self.initiative = roll(1, 20) + get_modifier(Ability.DEXTERITY)

    def roll_attack(self, target: Character, ability: Ability) -> bool:
        # TODO: Can we change the roll() method to notify us of natural 1's somehow?
        roll = roll(1, 20)
        if roll == 1: 
            return 1
        
        # Make this really simple for now.
        return roll + self.get_modifier(ability)

    def roll_death_save(self):
        death_save = roll(1, 20)
        # Natural 20 restores a hit point. No longer near death.
        if death_save == 20:
            self.current_hp = 1
            # Reset successes and failures.
            self.reset_death_saves()
        # Natural 1 counts as two failures.
        elif death_save == 1:
            self.death_save_failure += 2
        # 10 or more gives one success.
        elif death_save >= 10:
            self.death_save_success += 1
        # Else it's a failure.
        else:
            self.death_save_failure += 1

        # Check where we are.
        if self.death_save_success >= 3:
            # We've saved.
            self.current_hp = 1
            # Reset successes and failures.
            self.reset_death_saves()
        elif self.death_save_failure >= 3:
            self.current_hp = 0
            self.dead = True

    def reset_death_saves(self):
        self.death_save_failure = 0
        self.death_save_success = 0
