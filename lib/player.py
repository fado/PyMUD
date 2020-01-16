from lib.item import *


class Player(object):
    def __init__(self, name, health, inventory=Inventory()):
        self.name = name
        self.health = health
        self.inventory = inventory

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health += amount
