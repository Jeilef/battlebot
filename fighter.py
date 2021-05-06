import random
import numpy as np
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QWidget


class Fighter(QWidget):
    def __init__(self, num, flinkheit, initiative, parent):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.waffen = np.genfromtxt("data/waffen.csv", delimiter=";", dtype=str, encoding="utf-8")

        label_fighter = QLabel("Kämpfer " + str(num), self)
        label_fighter.move(10, 0)

        self.waffe1_fighter = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe1_fighter.addItem(self.waffen[row][0])
        self.waffe1_fighter.move(10, 30)

        self.waffe2_fighter = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe2_fighter.addItem(self.waffen[row][0])
        self.waffe2_fighter.move(10, 60)

        self.body_value = QLineEdit("Körperwert", self)
        self.body_value.move(10, 90)

        self.life_value = QLineEdit("Leben", self)
        self.life_value.move(10, 120)

        self.armor_value = QLineEdit("Rüstung", self)
        self.armor_value.move(10, 150)

        self.attack_dice_value = QLineEdit("Angriffswürfel", self)
        self.attack_dice_value.move(10, 180)

        self.dodge_dice_value = QLineEdit("Ausweichwürfel", self)
        self.dodge_dice_value.move(10, 240)

        self.dodge_chance = QLineEdit("Dodge Chance", self)
        self.dodge_chance.move(10, 270)

    def ausruesten(self):
        self.hand1 = self.waffen[self.waffe1_fighter.currentIndex()]
        self.hand2 = self.waffen[self.waffe2_fighter.currentIndex()]
        num_hands = int(self.hand1[10]) + int(self.hand2[10])    # gucken ob man genug hände hat
        if num_hands > 2:
            self.waffe2_fighter.setCurrentIndex(0)
            self.hand2 = self.waffen[0]
            print('Waffen auswahl nicht möglich')
        print(self.hand1, self.hand2)
        return self.hand1, self.hand2

    def angriff(self):
        angriffswert = int(self.body_value.text()) + int(self.hand1[7]) + int(self.hand2[7])
        if angriffswert >= random.randint(1, 21):                                     # Ob der Angriff trifft
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
            rand = random.randrange(0, 6)
            dmg += int(weapon[rand])
        return dmg

    def blocken(self, schaden):
        anzahl = int(self.hand1[8]) + int(self.hand2[8])
        threshold = 3
        blocks = [random.randrange(1, 7) for i in range(anzahl)]
        reduzierung = len(list(filter(lambda x: x <= threshold, blocks)))
        return max(0, schaden - int(self.armor_value.text()) - reduzierung)

    def ausweichen(self, schaden):
        if max([random.randrange(1, 7) for i in range(int(self.dodge_dice_value.text()))]) == 6:
            return 0
        else:
            return schaden - int(self.armor_value.text())