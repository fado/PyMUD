

class Dice():
    def __init__(self, sides, number, modifier):
        global finalroll
        finalroll = 0
        for x in range(0, number):
            roll = (randint(1, sides))
            finalroll = finalroll + roll
        modifiedroll = finalroll + modifier
        return modifiedroll

from random import randint
d = Dice()
d.__init__()
