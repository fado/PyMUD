from game_data import players, rooms, mud, game
from lib.models.client import Client
from lib.models.player import Player
from lib.mud_util import *

commands = dict()

# TODO: Tests. We probably need to mock the mudserver though,
# or somehow change these so they're not just side effects

def register_command(function):
    commands[function.__name__] = function
    return function


@register_command
def quit(client: Client, params=None):
    mud.disconnect(id)


@register_command
def help(client: Client, params=None):
    # send the player back the list of possible commands
    mud.send_message(client.uuid, "Commands:")
    mud.send_message(client.uuid, "  say <message>  - Says something out loud,"
                                  "e.g. 'say Hello'")
    mud.send_message(client.uuid, "  look           - Examines the "
                                  "surroundings, e.g. 'look'")
    mud.send_message(client.uuid, "  go <exit>      - Moves through the exit "
                                  "specified, e.g. 'go outside'")


@register_command
def say(player: Client, message):
    # go through every player in the game
    for other_player in players.values():
        # if they're in the same room as the player
        if other_player.room == player.room:
            # send them a message telling them what the player said
            mud.send_message(other_player, f"{player.name} says: {message}")


@register_command
def look(player: Player, params=None):
    # store the player's current room
    current_location = rooms[player.location]

    # send the player back the description of their current room
    tell_player(player, current_location['description'])

    playershere = []
    # go through every player in the game
    for other_player in game.players.values():
        # if they're in the same room as the player
        if other_player.location == player.location:
            # ... and they have a name to be shown
            if other_player.name:
                # add their name to the list
                playershere.append(other_player.name)

    # send player a message containing the list of players in the room
    tell_player(player, "Players here: {}".format(", ".join(playershere)))

    # send player a message containing the list of exits from this room
    tell_player(player, "Exits are: {}".format(", ".join(current_location["exits"])))


@register_command
def go(player: Player, params):
    # store the exit name   
    ex = params.lower()

    # store the player's current room
    current_location = rooms[player.location]

    # if the specified exit is found in the room's exits list
    if ex in current_location["exits"]:

        # go through all the players in the game
        for other_player in game.players.values():
            # if player is in the same room and isn't the player
            # sending the command
            if other_player.location == player.location and other_player.uuid != player.uuid:
                # send them a message telling them that the player
                # left the room
                tell_player(other_player.uuid, f"{player.name} left via exit '{ex}'")

        # update the player's current room to the one the exit leads to
        player.location = current_location["exits"][ex]
        current_location = rooms[player.location]

        # go through all the players in the game
        for other_player in game.players.values():
            # if player is in the same (new) room and isn't the player
            # sending the command
            if other_player.location == player.location and other_player.uuid != player.uuid:
                # send them a message telling them that the player
                # entered the room
                tell_player(other_player, f"{player.name} arrived via exit '{ex}'")

        # send the player a message telling them where they are now
        tell_player(player, "You arrive at '{player.location}'")

    # the specified exit wasn't found in the current room
    else:
        # send back an 'unknown exit' message
        tell_player(player, f"Unknown exit '{ex}'")
