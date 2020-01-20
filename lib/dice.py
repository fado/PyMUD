from random import randint
import re

class Dice():

    def split():
        numbers = re.split('[d+]', roll)
        return numbers

    @static def roll(self, numbers):
                for x in numbers:
                    try:
                        int(x)
                    except ValueError:
                        pass
                number = numbers[0]
                sides = numbers[1]
                modifier = numbers[2]
                finalroll = 0
                for x in range(0, number):
                    roll = (randint(1, sides))
                    finalroll = finalroll + roll
                modifiedroll = finalroll + modifier
                return modifiedroll