from typing import Dict

from mudserver import MudServer
from lib.models.player import Player

# TODO: Is there too much in this class now?
# The util didn't make sense anymore, because it was too tightly linked


class GameState(object):
    def __init__(self, server: MudServer):
        self.server = server
        self.players: Dict[str, Player] = {}

    def update(self):
        self.server.update()

    def add_player(self, player: Player):
        self.players[player.uuid] = player

    def remove_player(self, player: Player):
        del(self.players[player.uuid])

    def list_players(self):
        for player in self.players.values():
            yield player

    def list_other_players(self, exclude_player: Player):
        for player in self.list_players():
            if player.uuid != exclude_player.uuid:
                yield player

    def handle_player_join(self):
        for event in self.server.get_new_player_events():
            new_client = event.client
            new_player = Player(new_client, self.server)
            self.add_player(new_player)
            self.tell_player(new_player, "What is your name?")

    def handle_player_leave(self):
        for event in self.server.get_disconnected_player_events():
            disconnected_client = event.client
            disconnected_player = self.find_player_by_client_id(disconnected_client.uuid)
            if not disconnected_player:
                continue

            for player_id, player in self.players.items():
                self.tell_player(player, "{} quit the game".format(disconnected_player.name))

            self.remove_player(disconnected_player)

    def tell_player(self, player: Player, message: str):
        self.server.send_message(player.client.uuid, message)

    def broadcast(self, message: str):
        for player in self.players.values():
            self.tell_player(player, message)

    def find_player_by_client_id(self, client_id: str) -> Player:
        for player_id, player in self.players.items():
            if player.client.uuid == client_id:
                return player
