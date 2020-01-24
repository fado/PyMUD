import unittest
from unittest.mock import MagicMock

from lib.command import Commands
from lib.models.game_state import GameState
from lib.models.player import Player
from mudserver import MudServer
from test.fixtures.client_fixture import create_client_fixture
from test.fixtures.mock_server import MockServer


def command_class(mock_server: MudServer, num_clients: int = 2):
    commands = Commands(GameState(mock_server))
    for n in range(num_clients):
        player = Player(create_client_fixture(n), mock_server)
        player.name = "Player-%s" % n
        commands.game_state.add_player(player)
    return commands


class CommandTest(unittest.TestCase):
    @staticmethod
    def test_say():
        server = MockServer()
        server.send_message = MagicMock()

        commands = command_class(server)
        (player1, player2) = commands.game_state.players.values()

        commands.say(player1, "well")
        server.send_message.assert_called_with(
            player2.client.uuid, f"{player1.name} says: well"
        )


if __name__ == '__main__':
    unittest.main()
