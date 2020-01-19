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
        }

    def execute_command(self, player, command, param):
        print(self.commands)
        if self.commands.get(command):
            self.commands[command](player, param)
        else:
            self.game_state.tell_player(player, "Unknown command '{}'".format(command))

    def quit(self, player: Player, params=None):
        self.game_state.server.disconnect(player.client)

    def say(self, player: Player, message: str):
        # go through every player in the game
        for other_player in self.game_state.list_other_players(player):
            # if they're in the same room as the player
            if other_player.location == player.location:
                # send them a message telling them what the player said
                self.game_state.tell_player(other_player, f"{player.name} says: {message}")
        self.game_state.tell_player(player, f"You say: {message}")

    def help(self, player: Player, params=None):
        # send the player back the list of possible commands
        self.game_state.tell_player(player, "Commands:")
        self.game_state.tell_player(player, "  say <message>  - Says something out loud,"
                                            "e.g. 'say Hello'")
        self.game_state.tell_player(player, "  look           - Examines the "
                                            "surroundings, e.g. 'look'")
        self.game_state.tell_player(player, "  go <exit>      - Moves through the exit "
                                            "specified, e.g. 'go outside'")

    def look(self, player: Player, params=None):
        # store the player's current room
        current_location = rooms[player.location]

        # send the player back the description of their current room
        self.game_state.tell_player(player, current_location['description'])

        players_here = []
        # go through every player in the game
        for other_player in self.game_state.list_players():
            # if they're in the same room as the player
            if other_player.location == player.location:
                # ... and they have a name to be shown
                if other_player.name:
                    # add their name to the list
                    players_here.append(other_player.name)

        # send player a message containing the list of players in the room
        self.game_state.tell_player(player, "Players here: {}".format(", ".join(players_here)))
        # send player a message containing the list of exits from this room
        self.game_state.tell_player(player, "Exits are: {}".format(", ".join(current_location["exits"])))

    def go(self, player: Player, params):
        # store the exit name
        ex = params.lower()

        # store the player's current room
        current_location = rooms[player.location]

        # if the specified exit is found in the room's exits list
        if ex in current_location["exits"]:

            # go through all the players in the game
            for other_player in self.game_state.list_players():
                # if player is in the same room and isn't the player
                # sending the command
                if other_player.location == player.location and other_player.uuid != player.uuid:
                    # send them a message telling them that the player
                    # left the room
                    self.game_state.tell_player(other_player.uuid, f"{player.name} left via exit '{ex}'")

            # update the player's current room to the one the exit leads to
            player.location = current_location["exits"][ex]
            current_location = rooms[player.location]

            # go through all the players in the game
            for other_player in self.game_state.list_players():
                # if player is in the same (new) room and isn't the player
                # sending the command
                if other_player.location == player.location and other_player.uuid != player.uuid:
                    # send them a message telling them that the player
                    # entered the room
                    self.game_state.tell_player(other_player, f"{player.name} arrived via exit '{ex}'")

            # send the player a message telling them where they are now
            self.game_state.tell_player(player, f"You arrive at '{player.location}'")
            self.game_state.tell_player(player, rooms[player.location]["description"])

        # the specified exit wasn't found in the current room
        else:
            # send back an 'unknown exit' message
            self.game_state.tell_player(player, f"Unknown exit '{ex}'")
