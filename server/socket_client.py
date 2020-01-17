class SocketClient(object):
    """Holds information about a connected player"""

    # the socket object used to communicate with this client
    socket = None
    # the ip address of this client
    address = ""
    # holds data send from the client until a full message is received
    buffer = ""
    # the last time we checked if the client was still connected
    lastcheck = 0

    def __init__(self, socket, address, buffer, lastcheck):
        self.socket = socket
        self.address = address
        self.buffer = buffer
        self.lastcheck = lastcheck
