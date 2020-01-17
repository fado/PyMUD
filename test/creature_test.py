import unittest

from lib.models.character_class import CharacterClass
from lib.models.enums import Alignment, Ability, Skill
from lib.models.creature import Creature


class creatureTests(unittest.TestCase):

    @staticmethod
    def _createCreature():
        return Creature(
            name = 'Fado',
            description = 'Fado stands before you.',
            character_class = None,
            level = 4,
            background = "",
            race = "",
            alignment = Alignment.CHAOTIC_EVIL,
            xp = 0,
            abilities = {
                Ability.STRENGTH: 27,
                Ability.DEXTERITY: 14,
                Ability.CONSTITUTION: 12,
                Ability.WISDOM: 10,
                Ability.INTELLIGENCE: 7,
                Ability.CHARISMA: 3
            },
            skills = [
                Skill.PERCEPTION
            ],
            max_hp = 100,
            current_hp = 100,
            temporary_hp = 0,
            armor_class = 18,
            hd_value = 10,
            hd_total = 4,
        )

    def testTakeDamage(self):
        creature = self._createCreature()
        self.assertEqual(creature.take_damage(10), 90)

    def testHeal(self):
        creature = self._createCreature()
        self.assertEqual(creature.heal(10), 110)

    def testGetStrengthModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.STRENGTH), 8)

    def testGetDexModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.DEXTERITY), 2)

    def testGetConhModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.CONSTITUTION), 1)
    
    def testGetWisModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.WISDOM), 0)

    def testGetInthModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.INTELLIGENCE), -2)
    
    def testGetChaModifier(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_modifier(Ability.CHARISMA), -4)

    def testGetStrengthModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_strength_modifier(), 8)

    def testGetDexModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_dexterity_modifier(), 2)

    def testGetConhModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_constitution_modifier(), 1)
    
    def testGetWisModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_wisdom_modifier(), 0)

    def testGetInthModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_intelligence_modifier(), -2)
    
    def testGetChaModifierForHumans(self):
        creature = self._createCreature()
        self.assertEqual(creature.get_charisma_modifier(), -4)



if __name__ == '__main__':
    unittest.main()
