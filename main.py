import random
import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

from canvas import PlotCanvas
from fighter import Fighter


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

        self.hlayout = QHBoxLayout(self)

        self.start_battle_button = QPushButton("Start Battle", self)
        self.start_battle_button.move(250, 10)
        self.start_battle_button.clicked.connect(self.start_battle)


        # FIGHTER 1
        self.fighter1 = Fighter(0, 1, 1, self)

        # FIGHTER 2
        self.fighter2 = Fighter(1, 1, 1, self)

        # Fight process
        self.fight_diagram = PlotCanvas(self, width=5, height=4)
        self.fight_diagram.move(250, 80)

        self.hlayout.addWidget(self.fighter1)
        self.hlayout.addWidget(self.fight_diagram)
        self.hlayout.addWidget(self.fighter2)
        self.hlayout.addWidget(self.start_battle_button)


        self.show()

    @pyqtSlot()
    def start_battle(self):
        f1_damage_vals1 = self.waffen[self.waffe1_fighter_one.currentIndex()][1:7]
        f1_damage_vals2 = self.waffen[self.waffe2_fighter_one.currentIndex()][1:7]
        f2_damage_vals1 = self.waffen[self.waffe1_fighter_two.currentIndex()][1:7]
        f2_damage_vals2 = self.waffen[self.waffe2_fighter_two.currentIndex()][1:7]

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
            dmg_f1 = self.attack(f1_damage_vals1, f1_damage_vals2, int(self.dodge_dice_value_f1.text()),
                                 int(self.block_dice_value_f1.text()), float(self.dodge_chance_f1.text()))
            dmg_f1 -= int(self.armor_value_f1.text())
            f1_live_progress.append(f1_live_progress[-1] - max(0, dmg_f1))

            dmg_f2 = self.attack(f2_damage_vals1, f2_damage_vals2, int(self.dodge_dice_value_f2.text()),
                                 int(self.block_dice_value_f2.text()), float(self.dodge_chance_f2.text()))
            dmg_f2 -= int(self.armor_value_f2.text())
            f2_live_progress.append(f2_live_progress[-1] - max(0, dmg_f2))

        self.fight_diagram.plot(f1_live_progress, f2_live_progress)

    def attack(self, weapon1, weapon2, dodge_dice, dodge_chance):
        dmg = self.damage_roll(weapon1) + self.damage_roll(weapon2)
        if random.random() < dodge_chance:
            # dodge
            if max([random.randrange(1, 7) for i in range(dodge_dice)]) == 6:
                dmg = 0
        else:
            # block
            threshold = 3
            blocks = [random.randrange(1, 7) for i in range(block_dice)]
            dmg -= len(list(filter(lambda x: x <= threshold, blocks)))
        return dmg

    def damage_roll(self, weapon):
        rand = 0
        dmg = 0
        while rand == 0:
            rand = random.randrange(0, 6)
            dmg += int(weapon[rand])
        return dmg


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
