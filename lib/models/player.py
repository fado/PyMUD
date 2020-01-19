from dataclasses import dataclass

from lib.models.client import Client
from lib.models.creature import Creature


class Player(Creature):

    def __init__(self, client: Client, creature: Creature = None):
        self.client = client

        if creature:
            super().__init__(
                 creature.name,
                 creature.description,
                 creature.character_class,
                 creature.level,
                 creature.background,
                 creature.race,
                 creature.alignment,
                 creature.xp,
                 creature.abilities,
                 creature.skills,
                 creature.max_hp, 
                 creature.armor_class,
                 creature.hd_value,
                 creature.hd_total,
                 creature.inventory
            )

        super().__init__()
