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

        self.hundred_battles = QPushButton("Start 100 Battles", self)
        self.hundred_battles.move(250, 10)
        self.hundred_battles.clicked.connect(self.start_100_battles)


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
        self.hlayout.addWidget(self.hundred_battles)

        self.show()

    @pyqtSlot()
    def start_100_battles(self):
        for fight_num in range(100):
            hist1, hist2 = self.start_battle()
            with open("fights/fight" + str(fight_num), "w") as fight_hist:
                fight_hist.write(",".join(hist1) + "\n" + ",".join(hist2))

    @pyqtSlot()
    def start_battle(self):
        self.fighter1.ausruesten()
        self.fighter2.ausruesten()
        f1_live_progress = [int(self.fighter1.life_value.slider.value())]
        f2_live_progress = [int(self.fighter2.life_value.slider.value())]

        while f1_live_progress[-1] > 0 and f2_live_progress[-1] > 0:
            # FIGHT!!!
            dmg_f1 = self.fighter1.angriff()
            if random.random() < float(self.fighter2.dodge_chance.slider.value()):
                dmg_f1 = self.fighter2.ausweichen(dmg_f1)
            else:
                dmg_f1 = self.fighter2.blocken(dmg_f1)
            f2_live_progress.append(f2_live_progress[-1] - max(0, dmg_f1))

            dmg_f2 = self.fighter2.angriff()
            if random.random() < float(self.fighter1.dodge_chance.slider.value()):
                dmg_f2 = self.fighter1.ausweichen(dmg_f2)
            else:
                dmg_f2 = self.fighter1.blocken(dmg_f2)
            f1_live_progress.append(f1_live_progress[-1] - max(0, dmg_f2))

        self.fight_diagram.plot(f1_live_progress, f2_live_progress)
        return f1_live_progress, f2_live_progress


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
