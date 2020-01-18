from dataclasses import dataclass
from lib.models.client import Client
from server.server_enums import ServerEvents


@dataclass
class Event:
    event_type: ServerEvents
    client: Client
    command: str = ''
    params: str = ''
