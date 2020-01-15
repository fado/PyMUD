from models.item_classes import *


class Player(object):
    __default_health = 32

    def __init__(self, name, health=__default_health, inventory=Inventory()):
        self.name = name
        self.health = health
        self.inventory = inventory

    def take_damage(self, damage) -> int:
        self.health -= damage
        return self.health

    def heal(self, amount) -> int:
        self.health += amount
        return self.health
