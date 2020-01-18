
# TODO: Tests

def greet_players(player_list, mud):
    for event in mud.get_new_players():
        connected_player = event.client

        # add the new player to the dictionary, noting that they've not been
        # named yet.
        player_list[connected_player.uuid] = connected_player
        print(player_list)

        # send the new player a prompt for their name
        mud.send_message(connected_player.uuid, "What is your name?")


def remove_disconnected_players(player_list, mud):
    for event in mud.get_disconnected_players():
        player = event.client

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if player not in player_list:
            continue

        # TODO: This is probably broke
        # go through all the players in the game
        for pid, pl in player_list.items():
            # send each player a message to tell them about the disconnected
            # player
            mud.send_message(pid, "{} quit the game".format(
                player_list[player]["name"]))

        # remove the player's entry in the player dictionary
        del(player_list[player])
