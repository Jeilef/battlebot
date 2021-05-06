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

        # Fight process
        self.fight_diagram = PlotCanvas(self, width=5, height=4)
        self.fight_diagram.move(200, 80)

        self.show()

    @pyqtSlot()
    def start_battle(self):
        f1_damage_vals = self.waffen[self.waffe_fighter_one.currentIndex()][1:6]
        f2_damage_vals = self.waffen[self.waffe_fighter_two.currentIndex()][1:6]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())