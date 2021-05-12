import math
import random
import sys
import time

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

from Battleground import Battleground
from ValueSlider import ValueSlider
from canvas import PlotCanvas
from fighter import Fighter


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Battlebot'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 620
        self.waffen = None
        self.live_values_history = []
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
        self.start_battle_button.clicked.connect(self.store_fighter_data)
        self.start_battle_button.clicked.connect(self.start_battle)

        self.hundred_battles = QPushButton("Start 100 Battles", self)
        self.start_battle_button.clicked.connect(self.store_fighter_data)
        self.hundred_battles.clicked.connect(self.start_100_battles)

        self.toggle_round = QPushButton("Next Round", self)
        self.start_battle_button.clicked.connect(self.store_fighter_data)
        self.toggle_round.clicked.connect(self.toggle_battle_round)

        button_layout = QVBoxLayout(self)
        button_layout.addWidget(self.start_battle_button)
        button_layout.addWidget(self.hundred_battles)
        button_layout.addWidget(self.toggle_round)

        # Battleground
        self.battleground = Battleground(20, 401, self)

        # FIGHTERS
        self.vLayout = QVBoxLayout()

        self.num_fighters_sliders = ValueSlider(2, 4, 2, "Number of Fighters", self)
        self.num_fighters_sliders.slider.valueChanged.connect(self.add_fighter)
        self.vLayout.addWidget(self.num_fighters_sliders)

        self.fighter_selector = QComboBox(self)
        self.selected_fighter = 0
        self.add_fighter()
        self.fighter_selector.currentIndexChanged.connect(self.store_fighter_data)
        self.vLayout.addWidget(self.fighter_selector)

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

        self.flinkheit = ValueSlider(1, 10, 1, "Flinkheit", self)
        self.vLayout.addWidget(self.flinkheit)

        self.initiative = ValueSlider(10, 30, 1, "Initiative", self)
        self.vLayout.addWidget(self.initiative)


        diagram_layout = QVBoxLayout(self)

        # Fight process
        self.fight_diagram = PlotCanvas(self, width=4, height=4)

        diagram_layout.addWidget(self.fight_diagram)
        diagram_layout.addWidget(self.battleground)

        self.hlayout.addLayout(self.vLayout)
        self.hlayout.addLayout(diagram_layout)
        self.hlayout.addLayout(button_layout)

        self.show()

    @pyqtSlot()
    def store_fighter_data(self):
        fighter = list(self.battleground.fighters)[self.selected_fighter]
        fighter.waffe1_fighter = self.waffe1_fighter.currentIndex()
        fighter.waffe2_fighter = self.waffe2_fighter.currentIndex()
        fighter.body_value = self.body_value.slider.value()
        fighter.life_value = self.life_value.slider.value()
        fighter.armor_value = self.armor_value.slider.value()
        fighter.attack_dice_value = self.attack_dice_value.slider.value()
        fighter.dodge_dice_value = self.dodge_dice_value.slider.value()
        fighter.dodge_chance = self.dodge_chance.slider.value()
        fighter.flinkheit = self.flinkheit.slider.value()
        fighter.initiative = self.initiative.slider.value()
        self.selected_fighter = self.fighter_selector.currentIndex()
        self.battleground.selected_fighter = self.selected_fighter

    @pyqtSlot()
    def add_fighter(self):
        value = self.num_fighters_sliders.slider.value()
        while value != self.fighter_selector.count():
            print(self.fighter_selector.count(), value)
            if value > self.fighter_selector.count():
                self.fighter_selector.addItem("Fighter " + str(self.fighter_selector.count()))
                self.battleground.fighters.add(Fighter())
            else:
                self.fighter_selector.removeItem(self.fighter_selector.count() - 1)

    @pyqtSlot()
    def toggle_battle_round(self):
        if not self.live_values_history:
            for idx, f in enumerate(self.battleground.fighters):
                f.ausruesten()
                self.live_values_history.append([f.life_value])

        # FIGHT!!!
        self.battle_round(self.live_values_history)
        self.battleground.update()
        # time.sleep(2)

        self.fight_diagram.plot(self.live_values_history)

        if min(map(lambda x: x[-1], self.live_values_history)) <= 0:
            self.live_values_history.clear()

        return self.live_values_history

    @pyqtSlot()
    def start_100_battles(self):
        for fight_num in range(100):
            hist1, hist2 = self.start_battle()
            with open("fights/fight" + str(fight_num), "w") as fight_hist:
                fight_hist.write(",".join(hist1) + "\n" + ",".join(hist2))

    @pyqtSlot()
    def start_battle(self):
        live_values = []
        for idx, f in enumerate(self.battleground.fighters):
            f.ausruesten()
            live_values.append([f.life_value])

        while min(map(lambda x: x[-1], live_values)) > 0:
            # FIGHT!!!
            self.battle_round(live_values)
            self.battleground.update()
            # time.sleep(2)

        self.fight_diagram.plot(live_values)
        return live_values

    def battle_round(self, live_values):
        for idx, fighter in enumerate(self.battleground.fighters):
            target = sorted(self.battleground.fighters,
                             key=lambda f: math.sqrt(math.pow(fighter.x_pos - f.x_pos, 2) +
                                                     math.pow(fighter.y_pos - f.y_pos, 2)))[1]

            distance = math.sqrt(math.pow(fighter.x_pos - target.x_pos, 2) + math.pow(fighter.y_pos - target.y_pos, 2))
            table_value = "".join(filter(lambda x: x.isdigit(), self.waffen[fighter.waffe1_fighter][9]))
            reichweite = int(table_value) if table_value else 1
            if distance // self.battleground.cell_size <= reichweite:
                dmg = fighter.angriff()
                
                if random.random() < float(target.dodge_chance):
                    dmg = target.ausweichen(dmg)
                else:
                    dmg = target.blocken(dmg)
                
                live_values[idx].append(live_values[idx][-1] - max(0, dmg))
            else:
                movement = fighter.flinkheit * self.battleground.cell_size
                old_x_pos = fighter.x_pos
                if target.x_pos < fighter.x_pos - self.battleground.cell_size:
                    fighter.x_pos = fighter.x_pos - min(movement, fighter.x_pos - target.x_pos + self.battleground.cell_size)
                elif target.x_pos > fighter.x_pos + self.battleground.cell_size:
                    fighter.x_pos = fighter.x_pos + min(movement, target.x_pos - fighter.x_pos - self.battleground.cell_size)

                movement -= abs(old_x_pos - fighter.x_pos)
                if target.y_pos < fighter.y_pos - self.battleground.cell_size:
                    fighter.y_pos = fighter.y_pos - min(movement, fighter.y_pos - target.y_pos + self.battleground.cell_size)
                elif target.y_pos > fighter.y_pos + self.battleground.cell_size:
                    fighter.y_pos = fighter.y_pos + min(movement, target.y_pos - fighter.y_pos - self.battleground.cell_size)
                live_values[idx].append(live_values[idx][-1])


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
