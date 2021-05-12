from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget

import orderedset
from orderedset import OrderedSet


class Battleground(QWidget):
    def __init__(self, cells, size, parent):
        super().__init__(parent)
        self.pen = QPen()
        self.pen.setColor(QColor("black"))
        self.pen.setWidth(1)
        self.painter = QPainter(self)
        self.painter.setPen(self.pen)
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
        print("drawing")
        for f in self.fighters:
            self.painter.drawEllipse(f.x_pos,
                                     f.y_pos,
                                     half_cell_size, half_cell_size)

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        x_cell = (mouse_event.x() // self.cells) * self.cells
        y_cell = (mouse_event.y() // self.cells) * self.cells
        quarter_cell_size = (self.ground_size // (self.cells * 4))
        x_coord = x_cell + quarter_cell_size
        y_coord = y_cell + quarter_cell_size
        list(self.fighters)[self.selected_fighter].x_pos = x_coord
        list(self.fighters)[self.selected_fighter].y_pos = y_coord
        self.update()


