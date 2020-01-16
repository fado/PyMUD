# TODO: I think these should be in a separate directory

import unittest
from models import player_classes


class PlayerTests(unittest.TestCase):

    @staticmethod
    def _createPlayer():
        return player_classes.Player("fado", 100)

    def testTakeDamage(self):
        player = self._createPlayer()
        self.assertEqual(player.take_damage(10), 90)

    def testHeal(self):
        player = self._createPlayer()
        self.assertEqual(player.heal(10), 110)

if __name__ == '__main__':
    unittest.main()
