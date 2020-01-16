from lib.enums import ExitType

class Exit(Entity):
    def __init__(self, name, destination, description, exit_type: ExitType):
        self.destination = destination
        self.type = exit_type
        super().__init__(name, description)


class Room(Entity):
    def __init__(self, name, description, exits):
        self.exits = exits
        super().__init__(name, description)
