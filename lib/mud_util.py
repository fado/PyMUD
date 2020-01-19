from typing import List

from game_data import game, rooms
from lib.models.player import Player

# TODO: Tests

def handle_player_join():
    for event in game.server.get_new_player_events():
        
        new_client = event.client
        new_player = Player(new_client)

        game.add_player(new_player)

        tell_player(new_player, "What is your name?")


def handle_player_leave():
    for event in game.server.get_disconnected_player_events():
        
        disconnected_client = event.client

        disconnected_player = find_player_by_client_id(disconnected_client.uuid)
        if not disconnected_player:
            continue

        for player_id, player in game.players.items():
            tell_player(player, "{} quit the game".format(disconnected_player))

        game.remove_player(disconnected_player)


def tell_player(player: Player, message: str):
    game.server.send_message(player.client.uuid, message)


def broadcast(message: str):
    for player in game.players.values():
        tell_player(player, message)


def find_player_by_client_id(client_id: str) -> Player:
    for player_id, player in game.players.items():
        if player.client.uuid == client_id:
            return player
