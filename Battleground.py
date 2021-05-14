import math
import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget

import orderedset
from orderedset import OrderedSet


class Battleground(QWidget):
    def __init__(self, cells, size, parent):
        super().__init__(parent)
        self.colors = ["black", "red", "orange", "blue"]
        self.painter = QPainter(self)

        brush = QtGui.QBrush(QtCore.Qt.black)
        self.painter.setBrush(brush)
        self.selected_fighter = 0
        self.fighters = OrderedSet([])

        self.ground_size = size
        self.cell_size = size // cells
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.cells = cells
        self.draw_grid()

    def color_codes(self):
        return list(map(lambda x: QColor(x).name(), self.colors))

    def fight_finished(self, life_values):
        health_totals = {}
        for idx, f in enumerate(self.fighters):
            health_totals.setdefault(f.team, 0)
            health_totals[f.team] += life_values[idx][-1]
        return min(health_totals.values()) <= 0

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw_grid()
        self.painter.end()

    def draw_grid(self):
        for x_coord in range(0, self.ground_size + 1, self.ground_size // self.cells):
            self.painter.drawLine(x_coord, 0, x_coord, self.ground_size)
        for y_coord in range(0, self.ground_size + 1, self.ground_size // self.cells):
            self.painter.drawLine(0, y_coord, self.ground_size, y_coord)
        half_cell_size = (self.ground_size // (self.cells * 2))

        for idx, f in enumerate(self.fighters):
            pen = QPen()
            pen.setColor(QColor(self.colors[f.num]))
            pen.setWidth(1)
            self.painter.setPen(pen)
            self.painter.drawText(f.x_pos,
                                  f.y_pos,
                                  half_cell_size, half_cell_size, QtCore.Qt.AlignCenter, str(idx))

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        x_cell = (mouse_event.x() // self.cells) * self.cells
        y_cell = (mouse_event.y() // self.cells) * self.cells
        quarter_cell_size = (self.ground_size // (self.cells * 4))
        x_coord = x_cell + quarter_cell_size
        y_coord = y_cell + quarter_cell_size
        list(self.fighters)[self.selected_fighter].x_pos = x_coord
        list(self.fighters)[self.selected_fighter].y_pos = y_coord
        self.update()

    def find_target(self, fighter, f_idx, live_values):
        min_dist = self.ground_size * 2
        t_idx = 0
        for idx, target in enumerate(self.fighters):
            distance = math.sqrt(math.pow(fighter.x_pos - target.x_pos, 2) +
                                 math.pow(fighter.y_pos - target.y_pos, 2))
            if f_idx != idx and target.team != fighter.team and distance < min_dist and live_values[idx][-1] > 0:
                t_idx = idx
                min_dist = distance
        return t_idx

    def battle_round(self, live_values, waffen, fight_round):
        for idx, fighter in enumerate(self.fighters):
            if live_values[idx][-1] <= 0:
                continue
            t_idx = self.find_target(fighter, idx, live_values)
            target = self.fighters[t_idx]
            distance = math.sqrt(math.pow(fighter.x_pos - target.x_pos, 2) + math.pow(fighter.y_pos - target.y_pos, 2))
            table_value = "".join(filter(lambda x: x.isdigit(), waffen[fighter.waffe1_fighter][9]))
            reichweite = int(table_value) if table_value else 1
            if distance // self.cell_size <= reichweite:
                self.fighter_attacks(fight_round, fighter, live_values, t_idx, target)
            else:
                self.fighter_moves(fight_round, fighter, live_values, t_idx, target)
        # fill up life of all fighters that were not hit
        max_len = max(live_values, key=len)
        for lv in live_values:
            while len(lv) < len(max_len):
                lv.append(lv[-1])

    def fighter_moves(self, fight_round, fighter, live_values, t_idx, target):
        movement = fighter.flinkheit * self.cell_size
        old_x_pos = fighter.x_pos
        if target.x_pos < fighter.x_pos - self.cell_size:
            fighter.x_pos = fighter.x_pos - min(movement,
                                                fighter.x_pos - target.x_pos + self.cell_size)
        elif target.x_pos > fighter.x_pos + self.cell_size:
            fighter.x_pos = fighter.x_pos + min(movement,
                                                target.x_pos - fighter.x_pos - self.cell_size)
        movement -= abs(old_x_pos - fighter.x_pos)
        if target.y_pos < fighter.y_pos - self.cell_size:
            fighter.y_pos = fighter.y_pos - min(movement,
                                                fighter.y_pos - target.y_pos + self.cell_size)
        elif target.y_pos > fighter.y_pos + self.cell_size:
            fighter.y_pos = fighter.y_pos + min(movement,
                                                target.y_pos - fighter.y_pos - self.cell_size)
        if len(live_values[t_idx]) == fight_round:
            live_values[t_idx].append(live_values[t_idx][-1])

    def fighter_attacks(self, fight_round, fighter, live_values, t_idx, target):
        dmg = fighter.angriff()
        if random.random() < float(target.dodge_chance):
            dmg = target.ausweichen(dmg)
        else:
            dmg = target.blocken(dmg)
        if len(live_values[t_idx]) > fight_round:
            live_values[t_idx][-1] -= max(0, dmg)
        else:
            live_values[t_idx].append(live_values[t_idx][-1] - max(0, dmg))
