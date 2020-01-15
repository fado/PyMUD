

def greet_players(player_list, mud):
    for connected_player in mud.get_new_players():

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        # The dictionary key is the player's id number. We set their room to
        # None initially until they have entered a name
        # Try adding more player stats - level, gold, inventory, etc
        player_list[connected_player] = {
            "name": None,
            "room": None,
        }

        # send the new player a prompt for their name
        mud.send_message(connected_player, "What is your name?")


def remove_disconnected_players(player_list, mud):
    for player in mud.get_disconnected_players():

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if player not in player_list:
            continue

        # go through all the players in the game
        for pid, pl in player_list.items():
            # send each player a message to tell them about the disconnected
            # player
            mud.send_message(pid, "{} quit the game".format(
                player_list[player]["name"]))

        # remove the player's entry in the player dictionary
        del(player_list[player])
