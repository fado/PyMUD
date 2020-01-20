import uuid


class Client(object):
    def __init__(self, socket):
        self.uuid = uuid.uuid4()
        self.socket = socket
        # TODO: I just want a client to represent a socket initially
        self.name = None
        self.player = None
        self.room = None

