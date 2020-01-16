from game_data import players, rooms, mud


commands = dict()

def register_command(function):
    commands[function.__name__] = function
    return function


@register_command
def quit(id, params=None):
    mud.disconnect(id)

@register_command
def help(id, params=None):
    # send the player back the list of possible commands
    mud.send_message(id, "Commands:")
    mud.send_message(id, "  say <message>  - Says something out loud, "
                            + "e.g. 'say Hello'")
    mud.send_message(id, "  look           - Examines the "
                            + "surroundings, e.g. 'look'")
    mud.send_message(id, "  go <exit>      - Moves through the exit "
                            + "specified, e.g. 'go outside'")

@register_command
def say(id, params):
    # go through every player in the game
    for pid, pl in players.items():
        # if they're in the same room as the player
        if players[pid]["room"] == players[id]["room"]:
            # send them a message telling them what the player said
            mud.send_message(pid, "{} says: {}".format(players[id]["name"], params))

@register_command
def look(id, params=None):
    # store the player's current room
    rm = rooms[players[id]["room"]]

    # send the player back the description of their current room
    mud.send_message(id, rm["description"])

    playershere = []
    # go through every player in the game
    for pid, pl in players.items():
        # if they're in the same room as the player
        if players[pid]["room"] == players[id]["room"]:
            # ... and they have a name to be shown
            if players[pid]["name"] is not None:
                # add their name to the list
                playershere.append(players[pid]["name"])

    # send player a message containing the list of players in the room
    mud.send_message(id, "Players here: {}".format(", ".join(playershere)))

    # send player a message containing the list of exits from this room
    mud.send_message(id, "Exits are: {}".format(", ".join(rm["exits"])))

@register_command
def go(id, params):
    # store the exit name   
    ex = params.lower()

    # store the player's current room
    rm = rooms[players[id]["room"]]

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