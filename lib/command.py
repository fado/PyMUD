from game_data import rooms

from lib.models.player import Player

class CommandSet():

    def __init__(self, caller: Player, commands: Dict[str, Command]):
        self.caller = caller
        self.commands = commands


class PlayerCommandSet(CommandSet):

    def __init__(self, caller: Player):
        self.caller = caller
        commands = {
            'look'  : CommandLook(self.caller),
            'quit'  : CommandQuit(self.caller),
            'say'   : CommandSay(self.caller),
            'help'  : CommandHelp(self.caller),
            'go'    : CommandGo(self.caller)
        }
        
        super().__init__(caller, commands)


class Command(object):

    def __init__(self, caller: Player):
        self.caller = caller
        self.verb = verb


class CommandLook(Command):

    def __init__(self, caller: Player):
        super().__init__(caller)

    def call(self, params=None):
        current_location = rooms[self.caller.location]
        self.caller.message(current_location['description'])

        players_here = self.caller.search(SearchType.PLAYER)
        self.caller.message("Players here: {}".format(", ".join(players_here)))
        self.caller.message("Exits are: {}".format(", ".join(current_location["exits"])))
    

class CommandQuit(Command):

    def __init__(self, caller: Player):
        super().__init__(caller)

    def call(self, params=None):
        self.caller.disconnect()


class CommandSay(Command):

    def __init__(self, caller: Player):
        super().__init__(caller)

    def call(self, params=None):
        # Keep the variable name 'params' in the signature but convert it to
        # message for readability within this function.
        message = params

        if not message:
            self.caller.message("Say what?")
            return

        current_location = rooms[self.caller.location]
        players_here = self.caller.search(SearchType.PLAYER)

        for player in players_here:
            player.message(message)

        self.caller.message(f"You say: {params}")


class CommandHelp(Command):

    def __init__(self, caller: Player):
        super().__init__(caller)

    def call(self, params=None):
        self.caller.message("Commands:")
        self.caller.message("  say <message>  - Says something out loud, e.g. 'say Hello'")
        self.caller.message("  look           - Examines the surroundings, e.g. 'look'")
        self.caller.message("  go <exit>      - Moves through the exit specified, e.g. 'go outside'")


class CommandGo(Command):

    def __init__(self, caller: Player):
        super().__init__(caller)
    
    def call(self, params=None):
        current_location = rooms[self.caller.location]

        ex = params.lower()

        if ex in current_location['exits']:
            for other_player in self.caller.search(SearchType.PLAYER):
                other_player.message(f"{caller.name} left via exit '{ex}'")


            self.caller.location = current_location['exits'][ex]
            
            for other_player in self.caller.search(SearchType.PLAYER):
                other_player.message(f"{player.name} arrived via exit '{ex}'")

            self.caller.message(f"You arrive at '{player.location}'")
            self.caller.message(rooms[self.caller.location]["description"])
        
        else:
            self.caller.message(f"Unknown exit '{ex}'")
