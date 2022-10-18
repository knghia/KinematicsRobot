#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui,QtCore,QtWidgets

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtOpenGL import *

class PIDController:
    def __init__(self, *args, **kwargs):
        self.P = kwargs["P"]
        self.I = kwargs["I"]
        self.D = kwargs["D"]
        self.limit = kwargs["limit"]
        self.part_error = 0

        self.i = 0

    def get_output(self, error):
        p = self.P*error
        self.i += self.I*error

        if (self.i < -self.limit):
            self.i = -self.limit
        if (self.i > self.limit):
            self.i = self.limit

        d = self.D*(error-self.part_error)

        output = p+d+self.i
        
        if (output < -self.limit):
            output = -self.limit
        if (output > self.limit):
            output = self.limit

        self.part_error = error
        return output
        
Ra = 2
La = 0.23
Jm = 0.000052
Bm = 0.01
Kt = 0.235
Ke = 0.235
Kg = 0.01

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

class GraphicWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(GraphicWidget, self).__init__()
        self.setFixedSize(400,200)

        self.numberOfSamples = 1000
        pg.setConfigOptions(antialias=True)
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle(kwargs['name'], **{'color': '#FFFFFF'})
        self.plotWidget.getAxis('left').setTextPen('#FFFFFF')
        self.plotWidget.showGrid(x = True, y = True)
        self.plotWidget.setBackground((0x2E,0x31,0x38))
        self.plotWidget.setStyleSheet("border-radius: 10px;")
        
        horizontalLayout = QtWidgets.QVBoxLayout(self)
        horizontalLayout.addWidget(self.plotWidget)
        self.plotWidget.setYRange(kwargs['min'],kwargs['max'])
        self.plotWidget.getPlotItem().hideAxis('bottom')

        self.plotWidget.addLegend()
        self.timeArray = np.arange(-self.numberOfSamples, 0, 1)

        self.signalDataArrays = np.zeros(self.numberOfSamples)
        mpen = pg.mkPen(color=(0x8A,0xB6,0x1B), width=1.5)
        self.signalPlots = pg.PlotDataItem([0],[0],pen=mpen)
        self.plotWidget.addItem(self.signalPlots)

        self.setEnabled(False)

    def s16(self,value):
        return -(value & 0x8000) | (value & 0x7fff)

    def upDateGraphic(self, data):
        if data == None:
            return

        self.signalDataArrays = np.roll(self.signalDataArrays, -1)
        self.signalDataArrays[-1] = data
        self.updatePlot()
    
    def updatePlot(self):
        self.signalPlots.setData(self.timeArray, self.signalDataArrays)
        self.signalPlots.updateItems()

class InvalidValue(Exception):
    def __init__(self):
        Exception.__init__(self, "Not real solution")

h = 0.08
d = 0.04
l = 0.4
k = 0.12
xd = 0.4 - d
yd = 0

mB = 0.029
mb = 0.334
rB = 0.0095
JB = (2/5)*mB*rB**2
Jb = (1/3)*mB*l**2
g = 9.8

class DC_GlWidget(QGLWidget):
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(400, 400)

        self.U = 0
        self.part_U = 0
        self.delta_U = 0
        
        self.wt = self.func_wt(0)
        self.thetat = self.func_thetat(0)

        self.part_wt = self.wt
        self.part_thetat = self.thetat

        self.t = 0

        self.ts = 0
        self.tb = 0
        self.xt = 0
        self.xt0 = 0
        self.vt = 0
        self.vt0 = 0
        self.alpha = self.theta_2_alpha(self.thetat)
        self.part_alpha = 0

        # self.pid_alpha = PIDController(P=10, I=0, D=0, limit=2*np.pi)
        self.pid_alpha = PIDController(P=20, I=0, D=0, limit=74)
        self.pid_w = PIDController(P=0.2, I=0.8, D=0, limit=24)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

    def func_wt(self,t):
        return K*self.delta_U*(A2*np.exp(x1*t) + A3*np.exp(x2*t) - (A2+A3))

    def func_thetat(self,t):
        return K*self.delta_U*((A2/x1)*np.exp(x1*t) + (A3/x2)*np.exp(x2*t) - (A2+A3)*t - (A2/x1 + A3/x2))

    def theta_2_alpha(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        A = -2*(d*cos_theta+ xd)*l
        B = -2*(yd + d*sin_theta- h)*l
        C = k**2-(d*cos_theta+ xd)**2- (yd + d*sin_theta- h)**2- l**2
        delta = B**2+(A+C)*(A-C)
        t1 = (-B+np.sqrt(delta))/(-A-C)
        return np.arctan(t1)*2

    def drawGL(self):
        self.wt = self.func_wt(self.t) + self.part_wt
        self.thetat =  self.func_thetat(self.t)+ self.part_wt*(self.t)
        self.thetat = self.thetat + self.part_thetat

        if (self.U - self.part_U) != 0:
            self.delta_U = self.U - self.part_U
            self.part_wt = self.wt
            self.part_thetat = self.thetat
            self.part_U = self.U
            self.t = 0
            
        self.setupColor([0xE6, 0x3E, 0x31])
        # H
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(0,h)
        glVertex2f(0,0)
        glEnd()

        self.alpha = self.theta_2_alpha(self.thetat)
        cos_theta = np.cos(self.thetat)
        sin_theta = np.sin(self.thetat)
        cos_alpha = np.cos(self.alpha)
        sin_alpha = np.sin(self.alpha)

        glBegin(GL_LINES)
        # HB
        glVertex2f(0, h)
        glVertex2f(l*cos_alpha, h+ l*sin_alpha)
        # BC
        glVertex2f(l*cos_alpha, h+ l*sin_alpha)
        glVertex2f(xd+ d*cos_theta, yd+ d*sin_theta)
        # CD
        glVertex2f(xd+ d*cos_theta, yd+ d*sin_theta)
        glVertex2f(xd, yd)
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        zoom = 1
        glOrtho(-zoom, zoom, -zoom, zoom, -zoom, zoom)
        glMatrixMode(GL_MODELVIEW)

    def initializeGL(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glClearColor(187/255, 190/255, 191/255, 1.0)

    def draw_circle(self,x,y,r):
        sides = 32        
        glBegin(GL_POLYGON)    
        for i in range(100):    
            cosine= r * np.cos(i*2*np.pi/sides) + x    
            sine  = r * np.sin(i*2*np.pi/sides) + y    
            glVertex2f(cosine,sine)
        glEnd()
        
    def setupColor(self, color):
        color[0] = color[0]/255
        color[1] = color[1]/255
        color[2] = color[2]/255
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

    def upload_dc_motor(self, sp):
        self.t += 0.01
        wt_sp = self.pid_alpha.get_output(sp-self.alpha)
        self.U = self.pid_w.get_output(wt_sp - self.wt)
        self.updateGL()
        
class MainWindow(QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.setWindowTitle("DC Motor")
        self.dc_motor = DC_GlWidget(self)
        
        self.text_value_la = QtWidgets.QLabel(self)
        alpha_la = QtWidgets.QLabel(self)
        alpha_la.setText("Theta")
        self.alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.alpha_slider.setRange(-10,10)
        self.alpha_slider.setValue(0)
        self.alpha_slider.valueChanged.connect(self.load_text_value)
        self.text_value_la.setText(str(self.alpha_slider.value()))

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.start_time)

        self.speed_form = GraphicWidget(name="alpha",min= -10, max= 10)
        self.theta_form = GraphicWidget(name="Theta",min= -360, max= 360)

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.dc_motor)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(alpha_la)
        hbox.addWidget(self.alpha_slider)
        hbox.addWidget(self.text_value_la)
        hbox.addWidget(self.load_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        g_box.addWidget(self.speed_form)
        g_box.addWidget(self.theta_form)
        box.addLayout(g_box)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_handle)
        
    def start_time(self):
        self.timer.start(10)

    def time_handle(self):
        alpha_sp = self.alpha_slider.value()*np.pi/180
        self.dc_motor.upload_dc_motor(alpha_sp)
        self.theta_form.upDateGraphic(self.dc_motor.thetat*180/np.pi)
        self.speed_form.upDateGraphic(self.dc_motor.alpha*180/np.pi)

    def load_text_value(self,value):
        self.text_value_la.setText(str(value))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())