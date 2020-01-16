from lib.models.item import *


class Player(Entity):
    __default_health = 32

    def __init__(self, name, health=__default_health, inventory=Inventory()):
        self.health = health
        self.inventory = inventory
        # Set a default description, can allow the player to change it later.
        description = "They look fairly normal to you."
        super().__init__(name, description)

    def take_damage(self, damage) -> int:
        self.health -= damage
        return self.health

    def heal(self, amount) -> int:
        self.health += amount
        return self.health
