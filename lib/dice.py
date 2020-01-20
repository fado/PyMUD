from random import randint

class Dice():
    def roll(self, sides, number, modifier):
        finalroll = 0
        for x in range(0, number):
            roll = (randint(1, sides))
            finalroll = finalroll + roll
        modifiedroll = finalroll + modifier
        print(modifiedroll)
        return modifiedroll

d = Dice()
d.roll()