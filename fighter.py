import random
import numpy as np
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QWidget, QSlider, QVBoxLayout, QHBoxLayout

from ValueSlider import ValueSlider
from dice import Dice


class Fighter(QWidget):
    def __init__(self, num, flinkheit, initiative, parent):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.waffen = np.genfromtxt("data/waffen.csv", delimiter=";", dtype=str, encoding="utf-8")

        self.dice = None

        label_fighter = QLabel("Kämpfer " + str(num), self)
        label_fighter.move(10, 0)

        self.vLayout = QVBoxLayout()

        self.waffe1_fighter = QComboBox(self)
        for row in range(len(self.waffen)):
            self.waffe1_fighter.addItem(self.waffen[row][0])
        self.vLayout.addWidget(self.waffe1_fighter)

        self.waffe2_fighter = QComboBox(self)
        for row in range(len(self.waffen)):
            self.waffe2_fighter.addItem(self.waffen[row][0])
        self.vLayout.addWidget(self.waffe2_fighter)

        self.body_value = ValueSlider(6, 20, 10, "Körperwert", self)
        self.vLayout.addWidget(self.body_value)

        self.life_value = ValueSlider(30, 90, 10, "Leben", self, 3)
        self.vLayout.addWidget(self.life_value)

        self.armor_value = ValueSlider(0, 4, 1, "Rüstung", self)
        self.vLayout.addWidget(self.armor_value)

        self.attack_dice_value = ValueSlider(0, 4, 1, "Angriffswürfel", self)
        self.vLayout.addWidget(self.attack_dice_value)

        self.dodge_dice_value = ValueSlider(0, 8, 1, "Ausweichwürfel", self)
        self.vLayout.addWidget(self.dodge_dice_value)

        self.dodge_chance = ValueSlider(0, 1, 0.5, "Dodge Chance", self, 0.1)
        self.vLayout.addWidget(self.dodge_chance)

        self.setLayout(self.vLayout)

    def ausruesten(self):
        self.dice = Dice()
        self.hand1 = self.waffen[self.waffe1_fighter.currentIndex()]
        self.hand2 = self.waffen[self.waffe2_fighter.currentIndex()]
        num_hands = int(self.hand1[10]) + int(self.hand2[10])    # gucken ob man genug hände hat
        if num_hands > 2:
            self.waffe2_fighter.setCurrentIndex(0)
            self.hand2 = self.waffen[0]
            print('Waffen auswahl nicht möglich')
        return self.hand1, self.hand2

    def angriff(self):
        angriffswert = int(self.body_value.slider.value()) + int(self.hand1[7]) + int(self.hand2[7])
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
            rand = random.randrange(0, 6)
            dmg += int(weapon[rand])
        return dmg

    def blocken(self, schaden):
        anzahl = int(self.hand1[8]) + int(self.hand2[8])
        threshold = 3
        blocks = [random.randrange(1, 7) for i in range(anzahl)]
        reduzierung = len(list(filter(lambda x: x <= threshold, blocks)))
        return max(0, schaden - int(self.armor_value.slider.value()) - reduzierung)

    def ausweichen(self, schaden):
        if max([random.randrange(1, 7) for i in range(int(self.dodge_dice_value.slider.value()))]) == 6:
            return 0
        else:
            return schaden - int(self.armor_value.slider.value())