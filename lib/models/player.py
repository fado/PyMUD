from abc import ABC
from typing import List

import lib.command 

from lib.models.client import Client
from lib.models.creature import Creature


class Player(Creature, ABC):

    def __init__(self, 
                 client: Client, 
                 creature: Creature = None):
        self.client = client
        self.game_state = game_state
        self.cmdset = PlayerCommandSet(self)

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
        self.game_state.server.send_message(self.client.uuid, message)
    
    def has_command(self, verb) -> bool:
        return any(command for command in cmdset.commands if command.verb == verb)

    def call_command(self, verb, params):
        self.cmdset[verb](self, params)

    def search(self, type: SearchType, search_string: str = None):
        results = []

        if type == SearchType.PLAYER:
            for other_player in self.game_state.list_players():
                if other_player.location == self.location:
                    results.append(other_player)
            return results

    def disconnect(self):
        self.game_state.server.disconnect(self.client)
