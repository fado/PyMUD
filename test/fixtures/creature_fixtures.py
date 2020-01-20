from lib.models.creature import Creature
from lib.models.enums import Alignment, Ability, Skill


def create_creature_fixture():
    return Creature(
        name='Fado',
        description='Fado stands before you.',
        character_class=None,
        level=4,
        background="",
        race="",
        alignment=Alignment.CHAOTIC_EVIL,
        xp=0,
        abilities={
            Ability.STRENGTH: 27,
            Ability.DEXTERITY: 14,
            Ability.CONSTITUTION: 12,
            Ability.WISDOM: 10,
            Ability.INTELLIGENCE: 7,
            Ability.CHARISMA: 3
        },
        skills=[
            Skill.PERCEPTION
        ],
        max_hp=100,
        armor_class=18,
        hd_value=10,
        hd_total=4,
    )
