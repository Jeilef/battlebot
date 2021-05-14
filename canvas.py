import random

import matplotlib
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        super().__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data, colors):
        matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler('color', colors)
        self.figure.axes.clear()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for vals in data:
            ax.plot(range(len(vals)), vals)
        ax.set_title("Kampfgeschichte")
        ax.legend(list(map(lambda x: "Kämpfer " + str(x), range(len(data)))))
        self.draw()
