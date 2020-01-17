import unittest

from lib.models.character_class import CharacterClass
from lib.models.enums import Alignment, Ability, Skill
from lib.models.living import Living


class LivingTests(unittest.TestCase):

    @staticmethod
    def _createLiving():
        return Living(
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
        living = self._createLiving()
        self.assertEqual(living.take_damage(10), 90)

    def testHeal(self):
        living = self._createLiving()
        self.assertEqual(living.heal(10), 110)

    def testGetStrengthModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.STRENGTH), 8)

    def testGetDexModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.DEXTERITY), 2)

    def testGetConhModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.CONSTITUTION), 1)
    
    def testGetWisModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.WISDOM), 0)

    def testGetInthModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.INTELLIGENCE), -2)
    
    def testGetChaModifier(self):
        living = self._createLiving()
        self.assertEqual(living.get_modifier(Ability.CHARISMA), -4)

if __name__ == '__main__':
    unittest.main()
