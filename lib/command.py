from game_data import players, rooms, mud
from lib.models.client import Client

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
def look(player: Client, params=None):
    # store the player's current room
    rm = rooms[player.room]

    # send the player back the description of their current room
    mud.send_message(player.uuid, rm["description"])

    playershere = []
    # go through every player in the game
    for other_player in players.values():
        # if they're in the same room as the player
        if other_player.room == player.room:
            # ... and they have a name to be shown
            if other_player.name:
                # add their name to the list
                playershere.append(other_player.name)

    # send player a message containing the list of players in the room
    mud.send_message(player, "Players here: {}".format(", ".join(playershere)))

    # send player a message containing the list of exits from this room
    mud.send_message(player, "Exits are: {}".format(", ".join(rm["exits"])))


@register_command
def go(player: Client, params):
    # store the exit name   
    ex = params.lower()

    # store the player's current room
    rm = rooms[player.room]

    # if the specified exit is found in the room's exits list
    if ex in rm["exits"]:

        # go through all the players in the game
        for pid, pl in players.items():
            # if player is in the same room and isn't the player
            # sending the command
            if players[pid]["room"] == players[id]["room"] \
                    and pid != id:
                # send them a message telling them that the player
                # left the room
                mud.send_message(pid, "{} left via exit '{}'".format(
                                                players[id]["name"], ex))

        # update the player's current room to the one the exit leads to
        players[id]["room"] = rm["exits"][ex]
        rm = rooms[players[id]["room"]]

        # go through all the players in the game
        for pid, pl in players.items():
            # if player is in the same (new) room and isn't the player
            # sending the command
            if players[pid]["room"] == players[id]["room"] \
                    and pid != id:
                # send them a message telling them that the player
                # entered the room
                mud.send_message(pid, "{} arrived via exit '{}'".format(players[id]["name"], ex))

        # send the player a message telling them where they are now
        mud.send_message(id, "You arrive at '{}'".format(players[id]["room"]))

    # the specified exit wasn't found in the current room
    else:
        # send back an 'unknown exit' message
        mud.send_message(id, "Unknown exit '{}'".format(ex))