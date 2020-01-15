class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Inventory(object):
    def __init__(self):
        # Probably want to extend this so you can have many items of the same name
        self.inventory = {}

    def add_item(self, item: Item) -> str:
        self.inventory[item.name] = item
        return f"{item.name} added!"

    def remove_item(self, item: Item) -> str:
        i = self.inventory.get(item.name)
        if i:
            self.inventory.pop(item.name)
            return f"{item.name} removed!"
        else:
            return f"Inventory does not contain {item.name}"

    def has_item(self, item: Item) -> bool:
        return self.inventory.get(item.name) != False


class Weapon(Item):
    def __init__(self, name: str, description: str, damage: int):
        self.damage = damage
        super().__init__(name, description)
