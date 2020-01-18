from dataclasses import dataclass

from lib.models.client import Client
from lib.models.creature import Creature


class Player(Creature):

    def __init__(self, client: Client):
        self.client = client

        super().__init__()
