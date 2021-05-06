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

        self.hand1 = self.equip_weapon(self.hand1)
        self.hand2 = self.equip_weapon(self.hand2)
        hand = int(self.hand1[10]) + int(self.hand2[10])    # gucken ob man genug hände hat
        if hand > 2:
            self.hand1 = self.waffen[0]
            self.hand2 = self.waffen[0]
            print('Waffen auswahl nicht möglich')
        print(self.hand1, self.hand2)
        return self.hand1, self.hand2

    def equip_weapon(self, hand):
        for row in range(len(self.waffen)):
            if hand == self.waffen[row][0]:
                hand = self.waffen[row]
                break
            elif row == len(self.waffen) - 1:
                hand = self.waffen[1]
                break
        return hand

    def angriff(self):
        w20 = random.randint(1, 20)
        w6h1 = random.randint(1, 6)
        w6h2 = random.randint(1, 6)
        angriffswert = self.koerper + int(self.hand1[7]) + int(self.hand2[7])
        if angriffswert >= w20:                                     # Ob der Angriff trifft
            schaden1 = self.schadensberechnung(w6h1)
            schaden2 = self.schadensberechnung(w6h2)
            schaden = schaden1 + schaden2
            print(schaden, schaden1, schaden2)
        else:
            schaden = 0
            print(schaden)

    def schadensberechnung(self, w6):
        schaden = 0
        while w6 == 1:  # krit Ermittlung Waffe1
            if w6 == 1:
                w6 = random.randint(1, 6)
                schaden = schaden + int(self.hand1[1])
                print('+', self.hand1[1])
        schaden = schaden + int(self.hand1[w6])
        return(schaden1)

    def blocken(self,gegnerschaden):
        anzahl = int(self.hand1[8]) + int(self.hand2[8])
        blockwurf = []
        reduzierung = 0
        for wurf in range(0, anzahl):
            blockwurf.append(random.randint(1, 6))
            if blockwurf[wurf] <= 5:
                reduzierung = reduzierung + 1
                print(blockwurf,reduzierung)
        gegnerschaden = gegnerschaden - reduzierung

    def ausweichen(self,gegnerschaden):
        for wurf in range(0, 6):
            ausweichwurf = random.randint(1, 6)
            if ausweichwurf == 6:
                gegnerschaden = 0
                print(gegnerschaden)
                break
