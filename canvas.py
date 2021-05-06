import random

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data1, data2):
        self.figure.axes.clear()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data1, 'r-')
        ax.plot(data2, 'b-')
        ax.set_title("Kampfgeschichte")
        ax.legend(["Kämpfer 0", "Kämpfer 1"])
        self.draw()
