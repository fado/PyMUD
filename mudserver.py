"""Basic MUD server module for creating text-based Multi-User Dungeon
(MUD) games.

Contains one class, MudServer, which can be instantiated to start a
server running then used to send and receive messages from players.

author: Mark Frimston - mfrimston@gmail.com
"""

# TODO: Tests

import socket
import time

from lib.models.client import Client
from server.event import Event
from server.server_enums import *
from server.socket_server import SocketServer

from typing import List


class MudServer(object):
    """A basic server for text-based Multi-User Dungeon (MUD) games.

    Once created, the server will listen for players connecting using
    Telnet. Messages can then be sent to and from multiple connected
    players.

    The 'update' method should be called in a loop to keep the server
    running.
    """

    # list of occurrences waiting to be handled by the code
    _events: List[Event] = []
    # list of newly-added occurrences
    _new_events = []

    def __init__(self, interface="0.0.0.0", port=1234):
        """Constructs the MudServer object and starts listening for
        new players.
        """

        self._clients = {}
        self._events = []
        self._new_events = []
        # socket used to listen for new clients
        self._server_socket = SocketServer(interface, port)

    def update(self):
        """Checks for new players, disconnected players, and new
        messages sent from players. This method must be called before
        up-to-date info can be obtained from the 'get_new_players',
        'get_disconnected_players' and 'get_commands' methods.
        It should be called in a loop to keep the game running.
        """

        # check for new stuff
        self._check_for_new_connections()
        self._check_for_disconnected()
        self._check_for_messages()

        # move the new events into the main events list so that they can be
        # obtained with 'get_new_players', 'get_disconnected_players' and
        # 'get_commands'. The previous events are discarded
        self._events = list(self._new_events)
        self._new_events = []

    def get_new_player_events(self) -> List[Event]:
        """Returns a list containing info on any new players that have
        entered the game since the last call to 'update'. Each item in
        the list is a player id number.
        """
        return self.get_events(ServerEvents.NEW_PLAYER)

    def get_disconnected_player_events(self) -> List[Event]:
        """Returns a list containing info on any players that have left
        the game since the last call to 'update'. Each item in the list
        is a player id number.
        """
        return self.get_events(ServerEvents.PLAYER_LEFT)

    def get_commands(self) -> List[Event]:
        """Returns a list containing any commands sent from players
        since the last call to 'update'. Each item in the list is a
        3-tuple containing the id number of the sending player, a
        string containing the command (i.e. the first word of what
        they typed), and another string containing the text after the
        command
        """
        return self.get_events(ServerEvents.COMMAND)

    def get_events(self, event_type: ServerEvents) -> List[Event]:
        retval = []
        # go through all the events in the main list
        for ev in self._events:
            # if the event is a command occurrence, add the info to the list
            if ev.event_type == event_type:
                retval.append(ev)
        # return the info list
        return retval

    def send_message(self, to, message):
        """Sends the text in the 'message' parameter to the player with
        the id number given in the 'to' parameter. The text will be
        printed out in the player's terminal.
        """
        # we make sure to put a newline on the end so the client receives the
        # message on its own line
        # TODO: This isn't a nice interface
        if type(to) == Client:
            self._attempt_send(to.uuid, message+"\n\r")
        else:
            self._attempt_send(to, message+"\n\r")

    def shutdown(self):
        """Closes down the server, disconnecting all clients and
        closing the listen socket.
        """
        # for each client
        for cl in self._clients.values():
            # close the socket, disconnecting the client
            cl.socket.shutdown(socket.SHUT_RDWR)
            cl.socket.close()
        # stop listening for new clients
        self._server_socket.close()

    def disconnect(self, client: Client):
        client.socket.socket.shutdown(socket.SHUT_RDWR)

    def _attempt_send(self, clid, data):
        # look up the client in the client map and use 'sendall' to send
        # the message string on the socket. 'sendall' ensures that all of
        # the data is sent in one go
        client = self._clients.get(clid)
        try:
            if client:
                client.socket.send_to_client(data)
        # If there is a connection problem with the client (e.g. they have
        # disconnected) a socket error will be raised
        except socket.error:
            self._handle_disconnect(client)

    def _check_for_new_connections(self):
        new_client_socket = self._server_socket.check_for_new_clients()
        if new_client_socket:
            client = Client(new_client_socket)
            self._clients[client.uuid] = client
            self._new_events.append(
                Event(ServerEvents.NEW_PLAYER, client)
            )

    def _check_for_disconnected(self):

        # go through all the clients
        for player_id, cl in list(self._clients.items()):

            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - cl.socket.lastcheck < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(player_id, "\x00")

            # update the last check time
            cl.socket.lastcheck = time.time()

    def _check_for_messages(self):

        # go through all the clients
        for uid, client in self._clients.items():
            try:
                message = client.socket.check_for_messages(client)
                if message:
                    self._new_events.append(message)
            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(client)

    def _handle_disconnect(self, client: Client):
        # remove the client from the clients map
        del(self._clients[client.uuid])

        # add a 'player left' occurence to the new events list, with the
        # player's id number
        self._new_events.append(Event(ServerEvents.PLAYER_LEFT, client))
