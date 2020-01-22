from random import randint

    def roll(self, number, sides, modifier):
        finalroll = 0
        for x in range(0, number):
            roll = (randint(1, sides))
            finalroll = finalroll + roll
        modifiedroll = finalroll + modifier
        return modifiedroll