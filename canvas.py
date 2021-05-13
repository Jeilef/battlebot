import random

import matplotlib
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        super().__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler('color', ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                                                                             '#9467bd', '#8c564b',
                                                                             '#e377c2', '#7f7f7f', '#bcbd22',
                                                                             '#17becf'])
        self.figure.axes.clear()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for vals in data:
            ax.plot(range(len(vals)), vals)
        ax.set_title("Kampfgeschichte")
        ax.legend(list(map(lambda x: "Kämpfer " + str(x), range(len(data)))))
        self.draw()
