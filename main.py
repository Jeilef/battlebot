import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout

from Battleground import Battleground
from CustomWeaponPopup import CustomWeaponPopup
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
        self.start_battle_button.clicked.connect(self.start_battle)

        self.toggle_round = QPushButton("Next Round", self)
        self.toggle_round.clicked.connect(self.toggle_battle_round)

        button_layout = QVBoxLayout(self)
        button_layout.addWidget(self.start_battle_button)

        button_layout.addWidget(self.toggle_round)

        # Battleground
        self.battleground = Battleground(20, 401, self)

        # FIGHTERS
        self.vLayout = QVBoxLayout()

        self.add_custom_weapon_button = QPushButton("Add Weapon")
        self.add_custom_weapon_button.clicked.connect(self.add_custom_weapon)
        self.vLayout.addWidget(self.add_custom_weapon_button)

        self.num_fighters_sliders = ValueSlider(2, 4, 2, "Number of Fighters", self)
        self.num_fighters_sliders.slider.valueChanged.connect(self.add_fighter)
        self.vLayout.addWidget(self.num_fighters_sliders)

        self.fighter_selector = QComboBox(self)
        self.selected_fighter = 0
        self.add_fighter()
        self.fighter_selector.currentIndexChanged.connect(self.store_fighter_data)
        self.vLayout.addWidget(self.fighter_selector)

        self.team_selector = QComboBox(self)
        self.team_selector.addItems(list(map(lambda x: "Team " + str(x), range(4))))
        self.team_selector.currentIndexChanged.connect(self.store_fighter_data)
        self.vLayout.addWidget(self.team_selector)

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

        self.life_value = ValueSlider(30, 90, 30, "Leben", self, 3)
        self.vLayout.addWidget(self.life_value)

        self.armor_value = ValueSlider(0, 4, 1, "Rüstung", self)
        self.vLayout.addWidget(self.armor_value)

        self.attack_dice_value = ValueSlider(0, 4, 1, "Angriffswürfel", self)
        self.vLayout.addWidget(self.attack_dice_value)

        self.dodge_dice_value = ValueSlider(0, 8, 1, "Ausweichwürfel", self)
        self.vLayout.addWidget(self.dodge_dice_value)

        self.dodge_chance = ValueSlider(0, 10, 5, "Dodge Chance", self, 0.1)
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

        self.load_figher_data(self.battleground.fighters[self.selected_fighter])

        self.show()

    @pyqtSlot()
    def custom_weapon_created(self):
        print("custom weapon", self.popup.weapon)
        self.waffen = np.vstack((self.waffen, np.array(self.popup.weapon)))
        self.waffe1_fighter.addItem(self.popup.weapon[0])
        self.waffe2_fighter.addItem(self.popup.weapon[0])
        self.waffe1_fighter.update()
        self.waffe2_fighter.update()
        for f in self.battleground.fighters:
            f.waffen = self.waffen

    @pyqtSlot()
    def add_custom_weapon(self):
        self.popup = CustomWeaponPopup(self)
        self.popup.setGeometry(QRect(100, 100, 1200, 200))
        self.popup.new_weapon.connect(self.custom_weapon_created)
        self.popup.show()

    @pyqtSlot()
    def store_fighter_data(self):
        fighter = list(self.battleground.fighters)[self.selected_fighter]
        fighter.team = self.team_selector.currentIndex()
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
        print("selected fighter before", self.selected_fighter)
        self.selected_fighter = self.fighter_selector.currentIndex()
        print("selected fighter after", self.selected_fighter)
        self.load_figher_data(self.battleground.fighters[self.selected_fighter])

        self.battleground.selected_fighter = self.selected_fighter

    def load_figher_data(self, fighter):

        self.waffe1_fighter.setCurrentIndex(fighter.waffe1_fighter)
        self.waffe2_fighter.setCurrentIndex(fighter.waffe2_fighter)
        self.body_value.slider.setValue(fighter.body_value)
        self.life_value.slider.setValue(fighter.life_value)
        self.armor_value.slider.setValue(fighter.armor_value)
        self.attack_dice_value.slider.setValue(fighter.attack_dice_value)
        self.dodge_dice_value.slider.setValue(fighter.dodge_dice_value)
        self.dodge_chance.slider.setValue(fighter.dodge_chance)
        self.flinkheit.slider.setValue(fighter.flinkheit)
        self.initiative.slider.setValue(fighter.initiative)
        self.team_selector.setCurrentIndex(fighter.team)

    @pyqtSlot()
    def add_fighter(self):
        value = self.num_fighters_sliders.slider.value()
        while value != self.fighter_selector.count():
            print(self.fighter_selector.count(), value)
            if value > self.fighter_selector.count():
                self.fighter_selector.addItem("Fighter " + str(self.fighter_selector.count()))
                self.battleground.fighters.add(Fighter(self.waffen, self.fighter_selector.count() - 1))
            else:
                self.fighter_selector.removeItem(self.fighter_selector.count() - 1)

    @pyqtSlot()
    def toggle_battle_round(self):
        self.store_fighter_data()
        if not self.live_values_history:
            for idx, f in enumerate(self.battleground.fighters):
                f.ausruesten()
                self.live_values_history.append([f.life_value])

        # FIGHT!!!

        self.battleground.battle_round(self.live_values_history, self.waffen, len(self.live_values_history[0]))
        self.battleground.update()
        # time.sleep(2)

        self.fight_diagram.plot(self.live_values_history, self.battleground.color_codes())
        print(self.live_values_history, len(self.live_values_history[0]))
        if self.battleground.fight_finished(self.live_values_history):
            self.live_values_history.clear()

        return self.live_values_history

    @pyqtSlot()
    def start_battle(self):
        self.store_fighter_data()
        live_values = []
        for idx, f in enumerate(self.battleground.fighters):
            f.ausruesten()
            live_values.append([f.life_value])

        while not self.battleground.fight_finished(live_values):
            # FIGHT!!!
            round = len(live_values[0])
            self.battleground.battle_round(live_values, self.waffen, round)
            self.battleground.update()
            # time.sleep(2)

        self.fight_diagram.plot(live_values, self.battleground.color_codes())
        return live_values


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
