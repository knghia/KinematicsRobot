
import sys
from tracemalloc import start
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

class LSPB:
    def __init__(self,*args,**kwargs):
        self.t0 = 0
        self.tf = 0
        self.t = 0
        self.index = kwargs['t']

        self.q0 = 0
        self.qf = 0
        
        self.Vo = kwargs['V']
        self.V = 0
        self.tb = 0
        self.position = 0
        self.velocity = 0
        self.finish = True
        self.alpha = kwargs['alpha']

    def get_data(self,t):
        if (0< t <= self.tb):
            self.position = self.q0 + t**2*self.V/(2*self.tb)
            self.velocity = t*self.V/(self.tb)

        elif (self.tb < t <= (self.tf - self.tb)):
            self.position =  self.V*t + (self.qf + self.q0 - self.V*self.tf)/2
            self.velocity =  self.V

        elif ((self.tf - self.tb) < t < self.tf):
            self.position = self.qf- self.tf**2*self.V/(2*self.tb)+ t*self.V*self.tf/self.tb- t**2*self.V/(2*self.tb)
            self.velocity = self.V*self.tf/self.tb- t*self.V/(self.tb)

        return self.position,self.velocity

    def operation(self,*args,**kwargs):
        if (((self.t >= self.tf) or (self.t == 0)) and (self.finish == True)):
            self.q0 = kwargs['start']
            self.qf = kwargs['end']
            self.Vo = kwargs['Vo']

            if self.qf - self.q0 >= 0:
                self.V = self.Vo
            else:
                self.V = -self.Vo

            self.tf = self.alpha*(self.qf - self.q0)/self.V
            print(self.tf)
    
            self.tb = (self.q0 - self.qf + self.V*self.tf)/self.V
            self.t = 0
            self.finish = False

        if self.t < self.tf:
            self.t += self.index
            return self.t,self.get_data(self.t)
        else:
            self.t = 0
            self.finish = True
            return self.t,self.get_data(self.tf)

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

        self.setWindowTitle("LSPD")

        self.start_point = ParameterForm(name="Start", value=0, unit=" ")
        self.end_point = ParameterForm(name="End", value=100, unit=" ")
        self.velocity = ParameterForm(name="V", value=30, unit=" ")
        self.alpha = ParameterForm(name="⍺", value=1.2, unit="1<=⍺<=2")

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.update_plot)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.start_point)
        box_la.addWidget(self.end_point)
        box_la.addWidget(self.velocity)
        box_la.addWidget(self.alpha)
        box_la.addWidget(self.load_bt)

        self.graphics = MplCanvas(self, width=5, height=4, dpi=100)

        box = QtWidgets.QHBoxLayout(self)
        box.addLayout(box_la)
        box.addWidget(self.graphics)
        self.lspb = LSPB(V=self.velocity.get_value(), t=0.01, alpha=self.alpha.get_value())
        self.update_plot()

    def update_plot(self):
        self.graphics.axes.clear()
        self.lspb.alpha = self.alpha.get_value()
        time = []
        position = []
        while(1):
            t, p = self.lspb.operation(start=self.start_point.get_value(), end= self.end_point.get_value(), Vo=self.velocity.get_value())
            time.append(t)
            position.append(p)
            if (self.lspb.finish == True):
                break
        self.graphics.axes.plot(np.array(position))
        self.graphics.axes.set_xlim([0,1200])
        self.graphics.axes.grid(True)
        self.graphics.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
