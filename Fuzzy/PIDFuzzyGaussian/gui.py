
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QDoubleValidator

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

def gaussian_get_data(t,mu,sigma):
    up = -((t-mu)*(t-mu)/(2*sigma*sigma))
    g_x = np.exp(up)
    return g_x

class ParameterForm(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(ParameterForm,self).__init__()

        name = QtWidgets.QLabel(text=kwargs['name'])
        name.setAlignment(QtCore.Qt.AlignCenter)

        self.value_la =QtWidgets.QLineEdit(text=str(kwargs['value']))
        self.value_la.setValidator(QDoubleValidator())
        self.value_la.setAlignment(QtCore.Qt.AlignCenter)

        unit = QtWidgets.QLabel(text=kwargs['unit'])
        unit.setAlignment(QtCore.Qt.AlignCenter)

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(name)
        box.addWidget(self.value_la)
        box.addWidget(unit)

    def get_value(self):
        return float(self.value_la.text())

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Gaussian")
        self.mu = ParameterForm(name="mu", value=0, unit=" ")
        self.sigma = ParameterForm(name="sigma", value=5.31, unit=" ")

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.update_plot)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.mu)
        box_la.addWidget(self.sigma)
        box_la.addWidget(self.load_bt)
        self.graphics = MplCanvas(self, width=5, height=4, dpi=100)

        box = QtWidgets.QHBoxLayout(self)
        box.addLayout(box_la)
        box.addWidget(self.graphics)

    def update_plot(self):

        t = np.linspace(-40,40,5000)
        p = []
        mu = self.mu.get_value()
        sigma = self.sigma.get_value()

        for i in t:
            gau = gaussian_get_data(i, mu, sigma)
            p.append(gau)

        # self.graphics.axes.clear()
        self.graphics.axes.plot(t, p, label="t")
        self.graphics.axes.legend()
        self.graphics.axes.set_xlim([-40,40])
        self.graphics.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
