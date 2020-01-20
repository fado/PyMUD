import select
import socket
import time

from server.server_enums import ServerEvents
from server.socket_client import SocketClient


class SocketServer(object):
    def __init__(self, interface, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((interface, port))
        self.socket.setblocking(False)
        self.socket.listen(1)

    def check_for_new_clients(self):
        rlist, wlist, xlist = select.select([self.socket], [], [], 0)
        if self.socket not in rlist:
            return

        joined_socket, addr = self.socket.accept()
        joined_socket.setblocking(False)
        return SocketClient(joined_socket, addr[0], "", time.time())

    def close(self):
        self.socket.close()
