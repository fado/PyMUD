from abc import ABC

from lib.models.client import Client
from lib.models.creature import Creature
from mudserver import MudServer


class Player(Creature, ABC):

    def __init__(self, client: Client, server: MudServer, creature: Creature = None):
        self.client = client
        self.server = server

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


    def message(self, message):
        self.server.send_message(self.client.uuid, message)
