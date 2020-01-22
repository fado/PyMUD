from lib.models.entity import Room
from lib.models.enums import ExitType

rooms = {}

def add_room(room: Room):
    rooms[room.name] = room


# This is unpleasant to work with.

add_room(
    Room(name = 'tavern',
        description = "You're in a cozy tavern warmed by an open fire.",
        description_items = [
            Room.DescriptionItem(name = 'fire',
                            aliases = ['open fire'],
                            description = 'A warm, inviting fire.')
        ],
        exits = [
            Room.Exit(name = 'outside',
                description = 'A door leading to the outside.',
                destination = 'outside',
                exit_type = ExitType.DOOR)
        ]
    )
)


add_room(
    Room(name = 'outside',
        description = "You're standing outside a tavern. It's raining.",
        exits = [
            Room.Exit(
                name = 'inside',
                description = 'A door leading back inside.',
                destination = 'tavern',
                exit_type = ExitType.DOOR)
        ]
    )
)