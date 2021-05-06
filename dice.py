import random


class Dice:
    def __init__(self):
        self.w6_throws = {}
        self.w20_throws = {}

    def rollw6(self):
        roll = random.randint(1, 7)
        self.w6_throws.setdefault(roll, 0)
        self.w6_throws[roll] += 1
        return roll

    def rollw20(self):
        roll = random.randint(1, 21)
        self.w20_throws.setdefault(roll, 0)
        self.w20_throws[roll] += 1
        return roll
