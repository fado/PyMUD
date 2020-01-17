from server.server_enums import ReadState, TelnetCodes, TELNET_OPTION_CODES


def normal_read_state(message, state, buffer, character):
    # if we received the special 'interpret as command' code,
    # switch to 'command' state so that we handle the next
    # character as a command code and not as regular text data
    if ord(character) == TelnetCodes.INTERPRET_AS_COMMAND:
        state = ReadState.COMMAND
    # if we get a newline character, this is the end of the
    # message. Set 'message' to the contents of the buffer
    elif character == "\n":
        message = ''.join(buffer)

    # some telnet clients send the characters as soon as the user
    # types them. So if we get a backspace character, this is where
    # the user has deleted a character and we should delete the
    # last character from the buffer.
    elif character == "\x08":
        buffer = buffer[:-1]

    # otherwise it's just a regular character - add it to the
    # buffer where we're building up the received message
    else:
        buffer.append(character)
    return message, state, buffer


def subneg_read_state(message, state, buffer, character):
    # subnegotiation state

    # if we reach an 'end of subnegotiation' command, this ends the
    # list of options and we can return to 'normal' state.
    # Otherwise we must remain in this state
    if ord(character) == TelnetCodes.SUBNEGOTIATION_END:
        state = ReadState.NORMAL
    return message, state, buffer


def command_read_state(message, _, buffer, character):
    # command state
    # the special 'start of subnegotiation' command code indicates
    # that the following characters are a list of options until
    # we're told otherwise. We switch into 'subnegotiation' state
    # to handle this
    if ord(character) == TelnetCodes.SUBNEGOTIATION_START:
        state = ReadState.SUBNEG

    # if the command code is one of the 'will', 'wont', 'do' or
    # 'dont' commands, the following character will be an option
    # code so we must remain in the 'command' state
    elif ord(character) in TELNET_OPTION_CODES:
        state = ReadState.COMMAND

    # for all other command codes, there is no accompanying data so
    # we can return to 'normal' state.
    else:
        state = ReadState.NORMAL
    return message, state, buffer
