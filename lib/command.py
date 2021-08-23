from game_data import rooms
from lib.models.game_state import GameState

from lib.models.player import Player


class Commands(object):
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        # The register_command decorator was nicer, but it's harder to do inside a class
        # we can look at abstracting it out again, but we need to decide whether we want
        # state to be sent to every command if we do that, or manually register them so
        # they can be class methods (or do some other type of metaprogramming to register
        # them inside a class
        self.commands = {
            "quit": self.quit,
            "say": self.say,
            "help": self.help,
            "look": self.look,
            "go": self.go,
            "tell": self.tell,
        }

    def execute_command(self, player, command, param):
        if self.commands.get(command):
            self.commands[command](player, param)
        else:
            player.message("Unknown command '{}'".format(command))

    def quit(self, player: Player, params=None):
        """  quit           - Disconnects from the server"""
        self.game_state.server.disconnect(player.client)

    def say(self, player: Player, message: str):
        """  say <message>  - Says something out loud, e.g. 'say Hello'"""
        # go through every player in the game
        player.message(f"You say: {message}")
        for other_player in self.game_state.list_other_players(player):
            # if they're in the same room as the player
            if other_player._location == player._location:
                # send them a message telling them what the player said
                other_player.message(f"{player.name} says: {message}")

    def tell(self, player: Player, params):
        """ tell <player> message - Whisper a private message to the target player."""
        target = params.split(' ')[0]
        message = ' '.join(params.split(' ')[1:])

        if target.lower() not in [player.name.lower() for player in self.game_state.list_other_players(player)]:
            player.message("There is nobody online by that name.")

        for other_player in self.game_state.list_other_players(player):
            if other_player.name.lower() == target.lower():
                player.message(f"You whisper to {target}: {message}")
                other_player.message(f"{player.name} whispers to you: {message}")

    def help(self, player: Player, params=None):
        # send the player back the list of possible commands
        player.message("Commands:")
        for command in self.commands.values():
            if command.__doc__ is not None:
                player.message(command.__doc__)

    def look(self, player: Player, params=None):
        """  look           - Examines the surroundings, e.g. 'look'"""
        # store the player's current room
        current_location = rooms[player._location]

        # send the player back the description of their current room
        player.message(current_location.description)

        players_here = self._get_players_with(player)

        # send player a message containing the list of players in the room
        player.message("Players here: {}".format(", ".join([player.name for player in players_here])))
        # send player a message containing the list of exits from this room
        player.message("Exits are: {}".format(", ".join([ex.name for ex in current_location.exits])))

    def go(self, player: Player, params):
        """  go <exit>      - Moves through the exit specified, e.g. 'go outside'"""
        # store the exit name
        ex = params.lower()

        # store the player's current room
        current_location = rooms[player._location]

        # if the specified exit is found in the room's exits list
        if current_location.has_exit(ex):

            for other_player in self._get_players_with(player):
                other_player.message(f"{player.name} left via exit '{ex}'")

            # update the player's current room to the one the exit leads to
            player.move(current_location.get_exit(ex).destination)

            for other_player in self._get_players_with(player):
                other_player.message(f"{player.name} arrived via exit '{ex}'")

        # the specified exit wasn't found in the current room
        else:
            # send back an 'unknown exit' message
            player.message(f"Unknown exit '{ex}'")

    def _get_players_with(self, player: Player):
        players = []

        for uuid, item in rooms[player._location].inventory.get_items():
            if isinstance(item, Player) and item is not player:
                players.append(item)

        return players