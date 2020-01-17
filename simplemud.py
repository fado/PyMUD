#!/usr/bin/env python

"""A simple Multi-User Dungeon (MUD) game. Players can talk to each
other, examine their surroundings and move between rooms.

Some ideas for things to try adding:
    * More rooms to explore
    * An 'emote' command e.g. 'emote laughs out loud' -> 'Mark laughs
        out loud'
    * A 'whisper' command for talking to individual players
    * A 'shout' command for yelling to players in all rooms
    * Items to look at in rooms e.g. 'look fireplace' -> 'You see a
        roaring, glowing fire'
    * Items to pick up e.g. 'take rock' -> 'You pick up the rock'
    * Monsters to fight
    * Loot to collect
    * Saving players accounts between sessions
    * A password login
    * A shop from which to buy items

author: Mark Frimston - mfrimston@gmail.com
"""

import time

import mud_util
from game_data import mud, players, rooms
from command import commands


# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    mud.update()

    # go through any newly connected players
    mud_util.greet_players(players, mud)

    # go through any recently disconnected players
    mud_util.remove_disconnected_players(players, mud)

    # go through any new commands sent from players
    for event in mud.get_commands():
        client = event.client
        command = event.command
        params = event.params

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if client.uuid not in players:
            continue

        # if the player hasn't given their name yet, use this first command as
        # their name and move them to the starting room.
        if client.name is None:
            print("yet")

            client.name = command
            client.room = "Tavern"

            # go through all the players in the game
            for player in players.keys():
                # send each player a message to tell them about the new player
                mud.send_message(player, f"{client.name} entered the game")

            # send the new player a welcome message
            # TODO: A nicer interface to send_message so you don't need to do .uuid
            mud.send_message(client.uuid, f"Welcome to the game, {client.name}.")
            mud.send_message(client.uuid, "Type 'help' for a list of commands. Have fun!")
            mud.send_message(client.uuid, rooms[client.room]["description"])
            continue

        # each of the possible commands is handled below. Try adding new
        # commands to the game!

        if command in commands.keys():
            commands[command](client, params)

        # some other, unrecognised command
        else:
            # send back an 'unknown command' message
            mud.send_message(client, "Unknown command '{}'".format(command))
