
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

Ra = 2
La = 0.23
Jm = 0.000052
Bm = 0.01
Kt = 0.235
Ke = 0.235

a = 1
b = (Jm*Ra + La*Bm)/(La*Jm)
c = (Ke*Kt + Ra*Bm)/(La*Jm)

delta = b**2 - 4*a*c
x1 = (-b+np.sqrt(delta))/(2*a)
x2 = (-b-np.sqrt(delta))/(2*a)
K = Kt/(La*Jm)
A1 = 1/(x1*x2)
A2 = 1/(x1*(x1-x2))
A3 = 1/(x2*(x2-x1))

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

        self.Ra_la = ParameterForm(name="Ra", value=2, unit="Ω")
        self.La_la = ParameterForm(name="La", value=0.23, unit="H")
        self.Jm_la = ParameterForm(name="Jm", value=0.000052, unit="kg.m^2")
        self.Bm_la = ParameterForm(name="Bm", value=0.01, unit="N.m.s")
        self.Kt_la = ParameterForm(name="Kt", value=0.235, unit="N.m/A")
        self.Ke_la = ParameterForm(name="Ke", value=0.235, unit="V/rad/s")

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.update_plot)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.Ra_la)
        box_la.addWidget(self.La_la)
        box_la.addWidget(self.Jm_la)
        box_la.addWidget(self.Bm_la)
        box_la.addWidget(self.Kt_la)
        box_la.addWidget(self.Ke_la)
        box_la.addWidget(self.load_bt)

        self.graphics = MplCanvas(self, width=5, height=4, dpi=100)
        self.update_plot()

        box = QtWidgets.QHBoxLayout(self)
        box.addLayout(box_la)
        box.addWidget(self.graphics)

    def func_wt(self):
        t = np.linspace(0,2,2000)

        Ra = self.Ra_la.get_value()
        La = self.La_la.get_value()
        Jm = self.Jm_la.get_value()
        Bm = self.Bm_la.get_value()
        Kt = self.Kt_la.get_value()
        Ke = self.Ke_la.get_value()

        a = 1
        b = (Jm*Ra + La*Bm)/(La*Jm)
        c = (Ke*Kt + Ra*Bm)/(La*Jm)

        delta = b**2 - 4*a*c
        x1 = (-b+np.sqrt(delta))/(2*a)
        x2 = (-b-np.sqrt(delta))/(2*a)
        K = Kt/(La*Jm)
        A1 = 1/(x1*x2)
        A2 = 1/(x1*(x1-x2))
        A3 = 1/(x2*(x2-x1))

        return t,K*(A2*np.exp(x1*t) + A3*np.exp(x2*t) - (A2+A3))

    def update_plot(self):
        self.graphics.axes.clear()
        t,v = self.func_wt()
        self.graphics.axes.plot(t,v)
        self.graphics.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
