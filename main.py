import random
import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QLineEdit
from PyQt5.QtGui import QIcon

from canvas import PlotCanvas


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Battlebot'
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 620
        self.waffen = None
        self.read_weapons()
        self.initUI()

    def read_weapons(self):
        self.waffen = np.genfromtxt("data/waffen.csv", delimiter=";", dtype=str, encoding="utf-8")
        # col 0: Namen
        # col 1-6: Waffenschaden
        # col 7: Körpermod
        # col 8: Blockwürfel
        # col 9: Reichweite
        # col 10: Hände

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.start_battle_button = QPushButton("Start Battle", self)
        self.start_battle_button.move(250, 10)
        self.start_battle_button.clicked.connect(self.start_battle)

        # FIGHTER 1
        label_fighter_one = QLabel("Kämpfer 1", self)
        label_fighter_one.move(10, 0)

        self.waffe1_fighter_one = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe1_fighter_one.addItem(self.waffen[row][0])
        self.waffe1_fighter_one.move(10, 30)

        self.waffe2_fighter_one = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe2_fighter_one.addItem(self.waffen[row][0])
        self.waffe2_fighter_one.move(10, 60)

        self.body_value_f1 = QLineEdit("Körperwert", self)
        self.body_value_f1.move(10, 90)

        self.life_value_f1 = QLineEdit("Leben", self)
        self.life_value_f1.move(10, 120)

        self.armor_value_f1 = QLineEdit("Rüstung", self)
        self.armor_value_f1.move(10, 150)

        self.attack_dice_value_f1 = QLineEdit("Angriffswürfel", self)
        self.attack_dice_value_f1.move(10, 180)

        self.block_dice_value_f1 = QLineEdit("Blockwürfel", self)
        self.block_dice_value_f1.move(10, 210)

        self.dodge_dice_value_f1 = QLineEdit("Ausweichwürfel", self)
        self.dodge_dice_value_f1.move(10, 240)

        self.dodge_chance_f1 = QLineEdit("Dodge Chance", self)
        self.dodge_chance_f1.move(10, 270)

        # FIGHTER 2
        self.label_fighter_two = QLabel("Kämpfer 2", self)
        self.label_fighter_two.move(800, 0)

        self.waffe1_fighter_two = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe1_fighter_two.addItem(self.waffen[row][0])
        self.waffe1_fighter_two.move(800, 30)

        self.waffe2_fighter_two = QComboBox(self)
        for row in range(len(self.waffen)):
            print(self.waffen[row][0])
            self.waffe2_fighter_two.addItem(self.waffen[row][0])
        self.waffe2_fighter_two.move(800, 60)

        self.body_value_f2 = QLineEdit("Körperwert", self)
        self.body_value_f2.move(800, 90)

        self.life_value_f2 = QLineEdit("Leben", self)
        self.life_value_f2.move(800, 120)

        self.armor_value_f2 = QLineEdit("Rüstung", self)
        self.armor_value_f2.move(800, 150)

        self.attack_dice_value_f2 = QLineEdit("Angriffswürfel", self)
        self.attack_dice_value_f2.move(800, 180)

        self.block_dice_value_f2 = QLineEdit("Blockwürfel", self)
        self.block_dice_value_f2.move(800, 210)

        self.dodge_dice_value_f2 = QLineEdit("Ausweichwürfel", self)
        self.dodge_dice_value_f2.move(800, 240)

        self.dodge_chance_f2 = QLineEdit("Dodge Chance", self)
        self.dodge_chance_f2.move(800, 270)

        # Fight process
        self.fight_diagram = PlotCanvas(self, width=5, height=4)
        self.fight_diagram.move(200, 80)

        self.show()

    @pyqtSlot()
    def start_battle(self):
        f1_damage_vals1 = self.waffen[self.waffe1_fighter_one.currentIndex()][1:6]
        f1_damage_vals2 = self.waffen[self.waffe2_fighter_one.currentIndex()][1:6]
        f2_damage_vals1 = self.waffen[self.waffe1_fighter_two.currentIndex()][1:6]
        f2_damage_vals2 = self.waffen[self.waffe2_fighter_two.currentIndex()][1:6]

        handsf1_w1 = self.waffen[self.waffe1_fighter_one.currentIndex()][10]
        handsf2_w1 = self.waffen[self.waffe1_fighter_one.currentIndex()][10]

        if handsf1_w1 == 2:
            f1_damage_vals2 = np.zeros((6,))
        if handsf2_w1 == 2:
            f2_damage_vals2 = np.zeros((6,))

        f1_live_progress = [int(self.life_value_f1.text())]
        f2_live_progress = [int(self.life_value_f2.text())]

        while f1_live_progress[-1] > 0 and f2_live_progress[-1] > 0:
            # FIGHT!!!
            dmg_f1 = self.attack(f1_damage_vals1, f1_damage_vals2, self.dodge_dice_value_f1, self.block_dice_value_f1, self.dodge_chance_f1)
            dmg_f1 -= int(self.armor_value_f1)
            f1_live_progress.append(f1_live_progress[-1] - dmg_f1)

            dmg_f2 = self.attack(f2_damage_vals1, f2_damage_vals2, self.dodge_dice_value_f2, self.block_dice_value_f2, self.dodge_chance_f2)
            dmg_f2 -= int(self.armor_value_f2)
            f2_live_progress.append(f2_live_progress[-1] - dmg_f2)

        self.fight_diagram.plot(f1_live_progress, f2_live_progress)

    def attack(self, weapon1, weapon2, dodge_dice, block_dice, dodge_chance):
        dmg = weapon1[random.randrange(1,7)] + weapon2[random.randrange(1, 7)]
        if random.random() < dodge_chance:
            # dodge
            if max([random.randrange(1, 6) for i in range(dodge_dice)]) == 6:
                dmg = 0
        else:
            # block
            threshold = 3
            blocks = [random.randrange(1, 6) for i in range(block_dice)]
            dmg -= len(list(filter(lambda x: x <= threshold, blocks)))
        return dmg


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())