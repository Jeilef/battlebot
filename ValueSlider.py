from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QSlider, QHBoxLayout, QWidget, QLabel


class ValueSlider(QWidget):
    def __init__(self, min, max, start, var_name, parent, steps=1):
        super().__init__(parent)
        hlayout = QHBoxLayout(self)
        self.slider = QSlider(1, self)
        self.slider.setTickInterval(steps)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setSliderPosition(start)
        self.slider.valueChanged.connect(self.sliderChanged)

        self.var_name = var_name
        self.label = QLabel(var_name + " " + str(start), self)

        hlayout.addWidget(self.slider)
        hlayout.addWidget(self.label)
        self.setLayout(hlayout)

    @pyqtSlot()
    def sliderChanged(self):
        self.label.setText(self.var_name + " " + str(self.slider.value()))
