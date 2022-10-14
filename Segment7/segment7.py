
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

class Segment7:
    def __init__(self,*args,**kwargs):
        self.Amax = kwargs['A']
        self.Vmax = kwargs['V']
        self.Jmax = kwargs['J']
        self.index = kwargs['t']

        self.q0 = 0
        self.qf = 0

        self.T = 0
        self.t1 = 0
        self.t3 = 0
        self.t2 = 0
        self.t4 = 0
        self.t5 = 0
        self.t6 = 0

        self.a1 = self.Jmax
        self.a2 = 0
        self.a3 = -self.Jmax
        self.a4 = 0
        self.a5 = -self.Jmax
        self.a6 = 0
        self.a7 = self.Jmax

        self.position = 0
        self.velocity = 0
        self.t = 0
        self.finish = True

    def get_data(self,t):
        if ((0<t) and (t<= self.t1)):
            self.position = t*t*t*self.a1/6 + t*t*self.b1/2 + t*self.c1 +self.d1
            self.velocity = t*t*self.a1/2 + t*self.b1 + self.c1

        elif ((self.t1<t) and (t<= self.t2)):
            self.position = t*t*t*self.a2/6 + t*t*self.b2/2 + t*self.c2 +self.d2
            self.velocity = t*t*self.a2/2 + t*self.b2 + self.c2

        elif ((self.t2<t) and (t<= self.t3)):
            self.position = t*t*t*self.a3/6 + t*t*self.b3/2 + t*self.c3 +self.d3
            self.velocity = t*t*self.a3/2 + t*self.b3 + self.c3

        elif ((self.t3<t) and (t<= self.t4)):
            self.position = t*t*t*self.a4/6 + t*t*self.b4/2 + t*self.c4 +self.d4
            self.velocity = t*t*self.a4/2 + t*self.b4 + self.c4

        elif ((self.t4<t) and (t<= self.t5)):
            self.position = t*t*t*self.a5/6 + t*t*self.b5/2 + t*self.c5 +self.d5
            self.velocity = t*t*self.a5/2 + t*self.b5 + self.c5

        elif ((self.t5<t) and (t<= self.t6)):
            self.position = t*t*t*self.a6/6 + t*t*self.b6/2 + t*self.c6 +self.d6
            self.velocity = t*t*self.a6/2 + t*self.b6 + self.c6

        elif ((self.t6<t) and (t< self.T)):  
            self.position = t*t*t*self.a7/6 + t*t*self.b7/2 + t*self.c7 +self.d7
            self.velocity = t*t*self.a7/2 + t*self.b7 + self.c7

    def get_data(self,t):
        if ((0<t) and (t<= self.t1)):
            self.position = t*t*t*self.a1/6 + t*t*self.b1/2 + t*self.c1 +self.d1
            self.velocity = t*t*self.a1/2 + t*self.b1 + self.c1

        elif ((self.t1<t) and (t<= self.t2)):
            self.position = t*t*t*self.a2/6 + t*t*self.b2/2 + t*self.c2 +self.d2
            self.velocity = t*t*self.a2/2 + t*self.b2 + self.c2

        elif ((self.t2<t) and (t<= self.t3)):
            self.position = t*t*t*self.a3/6 + t*t*self.b3/2 + t*self.c3 +self.d3
            self.velocity = t*t*self.a3/2 + t*self.b3 + self.c3

        elif ((self.t3<t) and (t<= self.t4)):
            self.position = t*t*t*self.a4/6 + t*t*self.b4/2 + t*self.c4 +self.d4
            self.velocity = t*t*self.a4/2 + t*self.b4 + self.c4

        elif ((self.t4<t) and (t<= self.t5)):
            self.position = t*t*t*self.a5/6 + t*t*self.b5/2 + t*self.c5 +self.d5
            self.velocity = t*t*self.a5/2 + t*self.b5 + self.c5

        elif ((self.t5<t) and (t<= self.t6)):
            self.position = t*t*t*self.a6/6 + t*t*self.b6/2 + t*self.c6 +self.d6
            self.velocity = t*t*self.a6/2 + t*self.b6 + self.c6

        elif ((self.t6<t) and (t< self.T)):  
            self.position = t*t*t*self.a7/6 + t*t*self.b7/2 + t*self.c7 +self.d7
            self.velocity = t*t*self.a7/2 + t*self.b7 + self.c7

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def operation(self,*args,**kwargs):
        if (((self.t >= self.T) or (self.t == 0)) and (self.finish == True)):
        
            self.q0 = kwargs['q0']
            self.qf = kwargs['qf']

            self.Amax = kwargs['A']
            self.Vmax = kwargs['V']
            self.Jmax = kwargs['J']

            self.a1 = self.Jmax
            self.a2 = 0
            self.a3 = -self.Jmax
            self.a4 = 0
            self.a5 = -self.Jmax
            self.a6 = 0
            self.a7 = self.Jmax

            self.T = (self.Amax/self.Jmax) + (self.Vmax/self.Amax) + (self.qf/self.Vmax)
            
            self.t1 = self.Amax/self.Jmax
            self.t3 = self.t1 + (self.Vmax/self.Amax)
            self.t2 = self.t3 - self.t1

            self.t4 = self.T - self.t3
            self.t5 = self.T - self.t2
            self.t6 = self.T - self.t1

            self.b1 = 0
            self.b2 = self.Amax
            self.b3 = self.Amax + self.Jmax*self.t2
            self.b4 = 0
            self.b5 = self.Jmax*self.t4
            self.b6 = -self.Amax
            self.b7 = -self.Amax - self.Jmax*self.t6

            self.c1 = 0
            self.c2 = ((self.a1*self.t1**2)/2 + self.b1*self.t1 + self.c1) - ((self.a2*self.t1**2)/2 + self.b2*self.t1)
            self.c3 = ((self.a2*self.t2**2)/2 + self.b2*self.t2 + self.c2) - ((self.a3*self.t2**2)/2 + self.b3*self.t2)
            self.c4 = ((self.a3*self.t3**2)/2 + self.b3*self.t3 + self.c3) - ((self.a4*self.t3**2)/2 + self.b4*self.t3)
            self.c5 = ((self.a4*self.t4**2)/2 + self.b4*self.t4 + self.c4) - ((self.a5*self.t4**2)/2 + self.b5*self.t4)
            self.c6 = ((self.a5*self.t5**2)/2 + self.b5*self.t5 + self.c5) - ((self.a6*self.t5**2)/2 + self.b6*self.t5)
            self.c7 = ((self.a6*self.t6**2)/2 + self.b6*self.t6 + self.c6) - ((self.a7*self.t6**2)/2 + self.b7*self.t6)

            self.d1 = 0
            self.d2 = ((self.a1*self.t1**3)/6 + (self.b1*self.t1**2)/2 + self.c1*self.t1 + self.d1) - ((self.a2*self.t1**3)/6 + (self.b2*self.t1**2)/2 + self.c2*self.t1)
            self.d3 = ((self.a2*self.t2**3)/6 + (self.b2*self.t2**2)/2 + self.c2*self.t2 + self.d2) - ((self.a3*self.t2**3)/6 + (self.b3*self.t2**2)/2 + self.c3*self.t2)
            self.d4 = ((self.a3*self.t3**3)/6 + (self.b3*self.t3**2)/2 + self.c3*self.t3 + self.d3) - ((self.a4*self.t3**3)/6 + (self.b4*self.t3**2)/2 + self.c4*self.t3)
            self.d5 = ((self.a4*self.t4**3)/6 + (self.b4*self.t4**2)/2 + self.c4*self.t4 + self.d4) - ((self.a5*self.t4**3)/6 + (self.b5*self.t4**2)/2 + self.c5*self.t4)
            self.d6 = ((self.a5*self.t5**3)/6 + (self.b5*self.t5**2)/2 + self.c5*self.t5 + self.d5) - ((self.a6*self.t5**3)/6 + (self.b6*self.t5**2)/2 + self.c6*self.t5)
            self.d7 = ((self.a6*self.t6**3)/6 + (self.b6*self.t6**2)/2 + self.c6*self.t6 + self.d6) - ((self.a7*self.t6**3)/6 + (self.b7*self.t6**2)/2 + self.c7*self.t6)

            self.t = 0
            self.finish = False

        if self.t < self.T:
            self.t+= self.index
            self.get_data(self.t)
            return self.t, self.get_position(), self.get_velocity()
        else:
            self.t = 0
            self.finish = True
            self.get_data(self.T)
            return self.T, self.get_position(), self.get_velocity()

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

        self.setWindowTitle("Segment7")

        self.start_point = ParameterForm(name="Start", value=0, unit=" ")
        self.end_point = ParameterForm(name="End", value=100, unit=" ")
        self.v_max = ParameterForm(name="Vo", value=36, unit=" ")
        self.a_max = ParameterForm(name="Ao", value=20, unit=" ")
        self.j_max = ParameterForm(name="Jo", value=20, unit=" ")

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.update_plot)

        box_la = QtWidgets.QVBoxLayout()
        box_la.addWidget(self.start_point)
        box_la.addWidget(self.end_point)
        box_la.addWidget(self.v_max)
        box_la.addWidget(self.a_max)
        box_la.addWidget(self.j_max)
        box_la.addWidget(self.load_bt)

        self.graphics = MplCanvas(self, width=5, height=4, dpi=100)

        box = QtWidgets.QHBoxLayout(self)
        box.addLayout(box_la)
        box.addWidget(self.graphics)
        self.segment7 = Segment7(V=self.v_max.get_value(), A=self.a_max.get_value(),J=self.j_max.get_value(), t=0.01)
        self.update_plot()

    def update_plot(self):
        self.graphics.axes.clear()
        time = []
        position = []
        velocity = []
        while(1):
            t, p ,v = self.segment7.operation(
                q0=self.start_point.get_value(),
                qf= self.end_point.get_value(),
                V=self.v_max.get_value(),
                A=self.a_max.get_value(),
                J=self.j_max.get_value())

            time.append(t)
            position.append(p)
            velocity.append(v)
            if (self.segment7.finish == True):
                break
        self.graphics.axes.plot(time,position)
        self.graphics.axes.plot(time,velocity)
        # self.graphics.axes.set_xlim([0,200])
        self.graphics.axes.grid(True)
        self.graphics.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

