from typing import List

from lib.models.client import Client
from mudserver import MudServer, ServerEvents
from server.event import Event


class MockServer(MudServer):
    def __init__(self):
        pass

    def update(self):
        pass

    def get_new_player_events(self) -> List[Event]:
        pass

    def get_disconnected_player_events(self) -> List[Event]:
        pass

    def get_commands(self) -> List[Event]:
        pass

    def get_events(self, event_type: ServerEvents) -> List[Event]:
        pass

    def send_message(self, to, message):
        return to, message

    def shutdown(self):
        pass

    def disconnect(self, client: Client):
        pass

    def _attempt_send(self, clid, data):
        pass

    def _check_for_new_connections(self):
        pass

    def _check_for_disconnected(self):
        pass

    def _check_for_messages(self):
        pass

    def _handle_disconnect(self, client: Client):
        pass
