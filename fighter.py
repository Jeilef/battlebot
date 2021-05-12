import random

import numpy as np

from dice import Dice


class Fighter:
    def __init__(self):
        self.waffen = np.genfromtxt("data/waffen.csv", delimiter=";", dtype=str, encoding="utf-8")

        self.dice = None

        self.x_pos = 0
        self.y_pos = 0

        self.waffe1_fighter = 0
        self.waffe2_fighter = 0
        self.body_value = 0
        self.life_value = 0
        self.armor_value = 0
        self.attack_dice_value = 0
        self.dodge_dice_value = 0
        self.dodge_chance = 0
        self.flinkheit = 0
        self.initiative = 0

    def __hash__(self):
        return (self.x_pos, self.y_pos).__hash__()

    def ausruesten(self):
        self.dice = Dice()
        self.hand1 = self.waffen[self.waffe1_fighter]
        self.hand2 = self.waffen[self.waffe2_fighter]
        num_hands = int(self.hand1[10]) + int(self.hand2[10])    # gucken ob man genug hände hat
        if num_hands > 2:
            self.waffe2_fighter = 0
            self.hand2 = self.waffen[0]
            print('Waffen auswahl nicht möglich')
        return self.hand1, self.hand2

    def angriff(self):
        angriffswert = int(self.body_value) + int(self.hand1[7]) + int(self.hand2[7])
        if angriffswert >= random.randint(1, 20):                                     # Ob der Angriff trifft
            schaden1 = self.damage_roll(self.hand1[1:7])
            schaden2 = self.damage_roll(self.hand2[1:7])
            schaden = schaden1 + schaden2
        else:
            schaden = 0
        return schaden

    def damage_roll(self, weapon):
        rand = 0
        dmg = 0
        while rand == 0:
            rand = self.dice.rollw6() - 1
            dmg += int(weapon[rand])
        return dmg

    def blocken(self, schaden):
        anzahl = int(self.hand1[8]) + int(self.hand2[8])
        threshold = 3
        blocks = [random.randrange(1, 7) for i in range(anzahl)]
        reduzierung = len(list(filter(lambda x: x <= threshold, blocks)))
        return max(0, schaden - int(self.armor_value) - reduzierung)

    def ausweichen(self, schaden):
        if max([random.randrange(1, 7) for i in range(int(self.dodge_dice_value))]) == 6:
            return 0
        else:
            return schaden - int(self.armor_value)