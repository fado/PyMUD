from enum import Enum
# Used to store different types of occurences


class ServerEvents(Enum):
    NEW_PLAYER = 1
    PLAYER_LEFT = 2
    COMMAND = 3


class ReadState(Enum):
    NORMAL = 1
    COMMAND = 2
    SUBNEG = 3


# Command codes used by Telnet protocol
class TelnetCodes(Enum):
    INTERPRET_AS_COMMAND = 255
    ARE_YOU_THERE = 246
    WILL = 251
    WONT = 252
    DO = 253
    DONT = 254
    SUBNEGOTIATION_START = 250
    SUBNEGOTIATION_END = 240


TELNET_OPTION_CODES = (
    TelnetCodes.WILL,
    TelnetCodes.WONT,
    TelnetCodes.DO,
    TelnetCodes.DONT
)
