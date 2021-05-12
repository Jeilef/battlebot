import math

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QSlider, QHBoxLayout, QWidget, QLabel

from doubleslider import DoubleSlider


class ValueSlider(QWidget):
    def __init__(self, min, max, start, var_name, parent, steps=1):
        super().__init__(parent)
        hlayout = QHBoxLayout(self)
        if steps >= 1:
            self.slider = QSlider(1, self)
        else:
            self.slider = DoubleSlider(math.log10(1 / steps) // 1, 1, self)

        self.slider.setTickInterval(steps)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setSliderPosition(start)
        self.slider.valueChanged.connect(self.sliderChanged)



        self.step = steps
        self.var_name = var_name
        if steps >= 1:
            self.label = QLabel(var_name + " " + str(start), self)
        else:
            self.label = QLabel(var_name + " " + str(round(start * steps, 2)), self)

        hlayout.addWidget(self.slider)
        hlayout.addWidget(self.label)
        self.setLayout(hlayout)

    @pyqtSlot()
    def sliderChanged(self):
        if self.step >= 1:
            self.label.setText(self.var_name + " " + str(self.slider.value()))
        else:
            self.label.setText(self.var_name + " " + str(round(self.slider.value() * self.step, 2)))
