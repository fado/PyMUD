import unittest

from lib.models.entity import Inventory, Entity


class InventoryTest(unittest.TestCase):

    baseItem = Entity("sword", "big chungus")

    @staticmethod
    def _create_inventory():
        return Inventory()

    def test_add_item(self):
        inventory = self._create_inventory()
        inventory.add_item(self.baseItem)
        self.assertEqual(inventory.inventory[self.baseItem.uuid], self.baseItem)

    def test_has_item(self):
        inventory = self._create_inventory()
        inventory.add_item(self.baseItem)
        self.assertEqual(inventory.has_item(self.baseItem), True)

    def test_remove_Item(self):
        inventory = self._create_inventory()
        inventory.add_item(self.baseItem)
        inventory.remove_item(self.baseItem)
        self.assertEqual(
            inventory.inventory.get(self.baseItem.uuid),
            None
        )

if __name__ == '__main__':
    unittest.main()
