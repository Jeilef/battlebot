from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton


class CustomWeaponPopup(QWidget):
    new_weapon = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.vlayout = QVBoxLayout()
        self.table = QTableWidget(1, 11, self)
        self.vlayout.addWidget(self.table)

        self.confirm = QPushButton("Confirm", self)
        self.confirm.clicked.connect(self.confirm_weapon)
        self.vlayout.addWidget(self.confirm)
        self.setLayout(self.vlayout)

        self.weapon = []

    @pyqtSlot()
    def confirm_weapon(self):
        for i in range(0, self.table.columnCount()):
            self.weapon.append(self.table.item(0, i).text())
        self.new_weapon.emit()
        self.close()
        self.update()
