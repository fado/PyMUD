"""Basic MUD server module for creating text-based Multi-User Dungeon
(MUD) games.

Contains one class, MudServer, which can be instantiated to start a
server running then used to send and receive messages from players.

author: Mark Frimston - mfrimston@gmail.com
"""


import socket
import select
import time

from server.server_enums import *
from server.socket_client import SocketClient
from server import telnet_handler


class MudServer(object):
    """A basic server for text-based Multi-User Dungeon (MUD) games.

    Once created, the server will listen for players connecting using
    Telnet. Messages can then be sent to and from multiple connected
    players.

    The 'update' method should be called in a loop to keep the server
    running.
    """

    # Different states we can be in while reading data from client
    # See _process_sent_data function
    ReadState.NORMAL = 1
    _READ_STATE_COMMAND = 2
    _READ_STATE_SUBNEG = 3

    # Command codes used by Telnet protocol
    # See _process_sent_data function
    _TN_INTERPRET_AS_COMMAND = 255
    _TN_ARE_YOU_THERE = 246
    _TN_WILL = 251
    _TN_WONT = 252
    _TN_DO = 253
    _TN_DONT = 254
    _TN_SUBNEGOTIATION_START = 250
    _TN_SUBNEGOTIATION_END = 240

    # socket used to listen for new clients
    _listen_socket = None
    # holds info on clients. Maps client id to _Client object
    _clients = {}
    # counter for assigning each client a new id
    _nextid = 0
    # list of occurences waiting to be handled by the code
    _events = []
    # list of newly-added occurences
    _new_events = []

    def __init__(self, interface="0.0.0.0", port=1234):
        """Constructs the MudServer object and starts listening for
        new players.
        """

        self._clients = {}
        self._nextid = 0
        self._events = []
        self._new_events = []

        # create a new tcp socket which will be used to listen for new clients
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set a special option on the socket which allows the port to be
        # immediately without having to wait
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                       1)

        # bind the socket to an ip address and port. Port 23 is the standard
        # telnet port which telnet clients will use, however on some platforms
        # this requires root permissions, so we use a higher arbitrary port
        # number instead: 1234. Address 0.0.0.0 means that we will bind to all
        # of the available network interfaces
        self._listen_socket.bind((interface, port))

        # set to non-blocking mode. This means that when we call 'accept', it
        # will return immediately without waiting for a connection
        self._listen_socket.setblocking(False)

        # start listening for connections on the socket
        self._listen_socket.listen(1)

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

    def get_new_players(self):
        """Returns a list containing info on any new players that have
        entered the game since the last call to 'update'. Each item in
        the list is a player id number.
        """
        retval = []
        # go through all the events in the main list
        for ev in self._events:
            # if the event is a new player occurence, add the info to the list
            if ev[0] == ServerEvents.NEW_PLAYER:
                retval.append(ev[1])
        # return the info list
        return retval

    def get_disconnected_players(self):
        """Returns a list containing info on any players that have left
        the game since the last call to 'update'. Each item in the list
        is a player id number.
        """
        retval = []
        # go through all the events in the main list
        for ev in self._events:
            # if the event is a player disconnect occurence, add the info to
            # the list
            if ev[0] == ServerEvents.PLAYER_LEFT:
                retval.append(ev[1])
        # return the info list
        return retval

    def get_commands(self):
        """Returns a list containing any commands sent from players
        since the last call to 'update'. Each item in the list is a
        3-tuple containing the id number of the sending player, a
        string containing the command (i.e. the first word of what
        they typed), and another string containing the text after the
        command
        """
        retval = []
        # go through all the events in the main list
        for ev in self._events:
            # if the event is a command occurence, add the info to the list
            if ev[0] == ServerEvents.COMMAND:
                retval.append((ev[1], ev[2], ev[3]))
        # return the info list
        return retval

    def send_message(self, to, message):
        """Sends the text in the 'message' parameter to the player with
        the id number given in the 'to' parameter. The text will be
        printed out in the player's terminal.
        """
        # we make sure to put a newline on the end so the client receives the
        # message on its own line
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
        self._listen_socket.close()

    def disconnect(self, clid):
        self._clients[clid].socket.shutdown(socket.SHUT_RDWR)

    def _attempt_send(self, clid, data):
        # look up the client in the client map and use 'sendall' to send
        # the message string on the socket. 'sendall' ensures that all of
        # the data is sent in one go
        client = self._clients.get(clid)
        try:
            if client:
                client.socket.sendall(bytearray(data, "latin1"))
        # If there is a connection problem with the client (e.g. they have
        # disconnected) a socket error will be raised
        except socket.error:
            self._handle_disconnect(clid)

    def _check_for_new_connections(self):

        # 'select' is used to check whether there is data waiting to be read
        # from the socket. We pass in 3 lists of sockets, the first being those
        # to check for readability. It returns 3 lists, the first being
        # the sockets that are readable. The last parameter is how long to wait
        # - we pass in 0 so that it returns immediately without waiting
        rlist, wlist, xlist = select.select([self._listen_socket], [], [], 0)

        # if the socket wasn't in the readable list, there's no data available,
        # meaning no clients waiting to connect, and so we can exit the method
        # here
        if self._listen_socket not in rlist:
            return

        # 'accept' returns a new socket and address info which can be used to
        # communicate with the new client
        joined_socket, addr = self._listen_socket.accept()

        # set non-blocking mode on the new socket. This means that 'send' and
        # 'recv' will return immediately without waiting
        joined_socket.setblocking(False)

        # construct a new _Client object to hold info about the newly connected
        # client. Use 'nextid' as the new client's id number
        self._clients[self._nextid] =\
            SocketClient(joined_socket, addr[0], "", time.time())

        # add a new player occurence to the new events list with the player's
        # id number
        self._new_events.append((ServerEvents.NEW_PLAYER, self._nextid))

        # add 1 to 'nextid' so that the next client to connect will get a
        # unique id number
        self._nextid += 1

    def _check_for_disconnected(self):

        # go through all the clients
        for id, cl in list(self._clients.items()):

            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - cl.lastcheck < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(id, "\x00")

            # update the last check time
            cl.lastcheck = time.time()

    def _check_for_messages(self):

        # go through all the clients
        for id, cl in list(self._clients.items()):

            # we use 'select' to test whether there is data waiting to be read
            # from the client socket. The function takes 3 lists of sockets,
            # the first being those to test for readability. It returns 3 list
            # of sockets, the first being those that are actually readable.
            rlist, wlist, xlist = select.select([cl.socket], [], [], 0)

            # if the client socket wasn't in the readable list, there is no
            # new data from the client - we can skip it and move on to the next
            # one
            if cl.socket not in rlist:
                continue

            try:
                # read data from the socket, using a max length of 4096
                data = cl.socket.recv(4096).decode("latin1")

                # process the data, stripping out any special Telnet commands
                message = telnet_handler.process(cl, data)

                if message:
                    message = message.strip()

                    # separate the message into the command (the first word)
                    # and its parameters (the rest of the message)
                    command, params = (message.split(" ", 1) + ["", ""])[:2]

                    # add a command occurence to the new events list with the
                    # player's id number, the command and its parameters
                    self._new_events.append(
                        (ServerEvents.COMMAND, id, command.lower(), params)
                    )

            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(id)

    def _handle_disconnect(self, clid):

        # remove the client from the clients map
        del(self._clients[clid])

        # add a 'player left' occurence to the new events list, with the
        # player's id number
        self._new_events.append((ServerEvents.PLAYER_LEFT, clid))
