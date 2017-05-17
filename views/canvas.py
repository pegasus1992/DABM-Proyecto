from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy

from models.lectura import Lectura

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

LIM = 300


# Link: http://www.boxcontrol.net/embedding-matplotlib-plot-on-pyqt5-gui.html
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.resetValues()
        return

    def setPuerto(self, puerto):
        self.puerto = puerto
        return

    def resetValues(self):
        self.values = []
        self.i = 0
        self.setPuerto(None)
        self.lectura = None
        return

    def resetDrawing(self):
        self.resetValues()
        self.compute_initial_figure()
        return

    def compute_initial_figure(self):
        self.x, self.y = [], []
        for i in range(0, LIM + 1):
            self.x.append(i)
            self.y.append(0)
        self.axes.plot(self.x, self.y, 'r')
        return

    def update_figure(self):
        if self.puerto is not None:
            self.lectura = Lectura(self.puerto)
            self.puerto = None
        if self.lectura is not None:
            value = self.lectura.leer()
            self.values.append(value)
        if self.i < len(self.values):
            elem = self.values[self.i]
            self.y.append(elem)
            self.y.pop(0)
            self.i += 1
            self.axes.plot(self.x, self.y, 'r')
            self.draw()
        return
