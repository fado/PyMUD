from lib.models.enums import ExitType


class Exit(Entity):
    def __init__(self, name, description, destination, exit_type: ExitType):
        self.destination = destination
        self.type = exit_type
        super().__init__(name, description)


class DescriptionItem():
    '''Similar to Entity, but distinct in that you'll never be able to pick up
    a description item. It exists just for flavour text. Every noun in a room's
    description should have a corresponding description item.
    '''
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Room(Entity):
    def __init__(self, 
                 name: str, 
                 description: str,
                 description_items: List[DescriptionItems],
                 light_level: LightLevel = LightLevel.BRIGHT_LIGHT,
                 obscuration: Obscuration = Obscuration.NONE,
                 exits: List[Exit]):
        self.uuid = uuid.uuid4()
        self.description_items = description_items
        self.light_level = light_level
        self.obscuration = obscuration
        self.exits = exits

        super().__init__(name, description)


class World():
    '''TODO: Split rooms up by area.
    '''
    def __init__(self, rooms: List[Room] = None):
        self.rooms = rooms

    def add_room(self, room: Room):
        self.rooms.append(room)
