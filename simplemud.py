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

from game_data import rooms
from lib.command import Commands
from lib.models.game_state import GameState
from mudserver import MudServer

game = GameState(MudServer())
commands = Commands(game)

# Test PR.

# main game loop. We loop forever (i.e. until the program is terminated)
while True:

    # pause for 1/5 of a second on each loop, so that we don't constantly
    # use 100% CPU time
    time.sleep(0.2)

    # 'update' must be called in the loop to keep the game running and give
    # us up-to-date information
    game.update()

    # go through any newly connected players
    new_players = game.handle_player_join()

    # go through any recently disconnected players
    game.handle_player_leave()

    # go through any new commands sent from players
    for event in game.server.get_commands():
        client = event.client
        command = event.command
        params = event.params
        
        player = game.find_player_by_client_id(client.uuid)

        # if for any reason the player isn't in the player map, skip them and
        # move on to the next one
        if not player:
            continue

        if player.name is None:
            # Any new command event will become the player's name.
            player.name = command.capitalize()
    
            game.broadcast(f"{player.name} entered the game.")

            game.tell_player(player, f"Welcome to the game, {player.name}.")
            game.tell_player(player, "Type 'help' for a list of commands. Have fun!")
            game.tell_player(player, rooms[player.location].description)

            continue

        # each of the possible commands is handled below. Try adding new
        # commands to the game!
        commands.execute_command(player, command, params)
