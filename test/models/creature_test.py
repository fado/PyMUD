import unittest

from lib.models.enums import Ability
from test.fixtures.creature_fixtures import create_creature_fixture


class CreatureTests(unittest.TestCase):

    def testTakeDamage(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.take_damage(10), 90)

    def testHeal(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.heal(10), 110)

    def testGetStrengthModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.STRENGTH), 8)

    def testGetDexModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.DEXTERITY), 2)

    def testGetConhModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.CONSTITUTION), 1)
    
    def testGetWisModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.WISDOM), 0)

    def testGetInthModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.INTELLIGENCE), -2)
    
    def testGetChaModifier(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_modifier(Ability.CHARISMA), -4)

    def testGetStrengthModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_strength_modifier(), 8)

    def testGetDexModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_dexterity_modifier(), 2)

    def testGetConModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_constitution_modifier(), 1)
    
    def testGetWisModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_wisdom_modifier(), 0)

    def testGetIntModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_intelligence_modifier(), -2)
    
    def testGetChaModifierForHumans(self):
        creature = create_creature_fixture()
        self.assertEqual(creature.get_charisma_modifier(), -4)


if __name__ == '__main__':
    unittest.main()
