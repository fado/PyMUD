from lib.item import *


class Player(Entity):
    def __init__(self, name, health, inventory=Inventory()):
        self.health = health
        self.inventory = inventory
        # Set a default description, can allow the player to change it later.
        description = "They look fairly normal to you."
        super().__init__(name, description)

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health += amount
