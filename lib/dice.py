from random import randint

def roll(self, number, sides, modifier = 0):
    finalroll = 0
    for x in range(number):
        roll = (randint(1, sides))
        finalroll += roll
    return finalroll + modifier
