from server.telnet_actions.actions import *

_MAPPINGS = {
    ReadState.NORMAL: normal_read_state,
    ReadState.SUBNEG: subneg_read_state,
    ReadState.COMMAND: command_read_state
}


def process(data):
    # the Telnet protocol allows special command codes to be inserted into
    # messages. For our very simple server we don't need to response to
    # any of these codes, but we must at least detect and skip over them
    # so that we don't interpret them as text data.
    # More info on the Telnet protocol can be found here:
    # http://pcmicro.com/netfoss/telnet.html

    # start with no message and in the normal state
    message = None
    state = ReadState.NORMAL

    buffer = []
    for character in data:
        message, state, buffer = _MAPPINGS[state](message, state, buffer, character)
    return message
