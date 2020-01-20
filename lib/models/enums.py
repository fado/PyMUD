from enum import Enum


class Obscuration(Enum):
    NONE = 'None'
    LIGHT = 'lightly obscured'
    HEAVY = 'heavily obscured'


class LightLevel(Enum):
    BRIGHT = 'bright light'
    DIM = 'dim light'
    DARKNESS = 'darkness'


class ExitType(Enum):
    DOOR = 'door'
    PATH = 'path'
    ROAD = 'road'
    CORRIDOR = 'corridor'


class Ability(Enum):
    STRENGTH = 'Strength'
    DEXTERITY = 'Dexterity'
    CONSTITUTION = 'Constitution'
    INTELLIGENCE = 'Intelligence'
    WISDOM = 'Wisdom'
    CHARISMA = 'Charisma'


class Skill(Enum):
    ACROBATICS = ('Acrobatics', Ability.DEXTERITY)
    ANIMAL_HANDLING = ('Animal Handling', Ability.WISDOM)
    ARCANA = ('Arcana', Ability.INTELLIGENCE)
    ATHLETICS = ('Athletics', Ability.STRENGTH)
    DECEPTION = ('Deception', Ability.CHARISMA)
    HISTORY = ('History', Ability.INTELLIGENCE)
    INSIGHT = ('Insight', Ability.WISDOM)
    INTIMIDATION = ('Intimidation', Ability.CHARISMA)
    INVESTIGATION = ('Investigation', Ability.INTELLIGENCE)
    MEDICINE = ('Medicine', Ability.WISDOM)
    NATURE = ('Nature', Ability.INTELLIGENCE)
    PERCEPTION = ('Perception', Ability.WISDOM)
    PERFORMANCE = ('Performance', Ability.CHARISMA)
    PERSUASION = ('Persuasion', Ability.CHARISMA)
    RELIGION = ('Religion', Ability.INTELLIGENCE)
    SLEIGHT_OF_HAND = ('Sleight of Hand', Ability.DEXTERITY)
    STEALTH = ('Stealth', Ability.DEXTERITY)
    SURVIVAL = ('Survival', Ability.WISDOM)


class Alignment(Enum):
    LAWFUL_GOOD = 'Lawful Good'
    NEUTRAL_GOOD = 'Neutral Good'
    CHAOTIC_GOOD = 'Chaotic Good'
    LAWFUL_NEUTRAL = 'Lawful Neutral'
    NEUTRAL = 'Neutral'
    CHAOTIC_NEUTRAL = 'Chaotic Neutral'
    LAWFUL_EVIL = 'Lawful Evil'
    NEUTRAL_EVIL = 'Neutral Evil'
    CHAOTIC_EVIL = 'Chaotic Evil'


class ArmorType(Enum):
    LIGHT = 'Light Armor'
    MEDIUM = 'Medium Armor'
    HEAVY = 'Heavy Armor'
    SHIELD = 'Shield'


class WeaponType(Enum):
    SIMPLE = 'Simple'
    MARTIAL = 'Martial'
