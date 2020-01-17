import unittest

from lib.models.player import Player


class PlayerTests(unittest.TestCase):

    @staticmethod
    def _create_player():
        return Player("fado", 100)

    def test_take_damage(self):
        player = self._create_player()
        self.assertEqual(player.take_damage(10), 90)

    def test_heal(self):
        player = self._create_player()
        self.assertEqual(player.heal(10), 110)

if __name__ == '__main__':
    unittest.main()
