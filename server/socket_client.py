import select
from typing import Optional, Tuple

from server import telnet_handler
from server.event import Event
from server.server_enums import ServerEvents


class SocketClient(object):
    """Network state for a connected player"""

    def __init__(self, socket, address, buffer, lastcheck):
        self.socket = socket
        self.address = address
        self.buffer = buffer
        self.lastcheck = lastcheck

    def send_to_client(self, message):
        self.socket.sendall(bytearray(message, "latin1"))

    def check_for_messages(self, client) -> Event:
        rlist, wlist, xlist = select.select([self.socket], [], [], 0)
        if self.socket not in rlist:
            return
        data = self.socket.recv(4096).decode("latin1")
        message = telnet_handler.process(data)

        if message:
            message = message.strip()
            # separate the message into the command (the first word)
            # and its parameters (the rest of the message)
            command, params = (message.split(" ", 1) + ["", ""])[:2]
            return Event(ServerEvents.COMMAND, client, command.lower(), params)

