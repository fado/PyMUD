from typing import List, Dict

from mudserver import MudServer
from lib.models.player import Player


# structure defining the rooms in the game. Try adding more rooms to the game!
rooms = {
    "Tavern": {
        "description": "You're in a cozy tavern warmed by an open fire.",
        "exits": {"outside": "Outside"},
    },
    "Outside": {
        "description": "You're standing outside a tavern. It's raining.",
        "exits": {"inside": "Tavern"},
    }
}

players: List[Player] = []

# start the server
mud = MudServer()


class Game():
    def __init__(self):
        self.players: Dict[str, Player] = {}

    def add_player(self, player: Player):
        self.players[player.uuid] = player

    def remove_player(self, player: Player):
        del(self.players[player.uuid])


game = Game()