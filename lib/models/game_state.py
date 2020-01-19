from typing import Dict

from mudserver import MudServer
from lib.models.player import Player


class GameState():
    def __init__(self, server: MudServer):
        self.server = server
        self.players: Dict[str, Player] = {}

    def update(self):
        self.server.update()

    def add_player(self, player: Player):
        self.players[player.uuid] = player

    def remove_player(self, player: Player):
        del(self.players[player.uuid])