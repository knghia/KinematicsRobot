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
h1 = 0.0
l = 0.4
d = 0.04
k = 0.08
xd = 0.4 - d

class DC_GlWidget(QGLWidget):
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(400, 400)

        self.theta = 0
        self.alpha = 0

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

    def drawGL(self):  
        glPushMatrix()
        self.setupColor([0xE6, 0x3E, 0x31])
        # H
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(0,h)
        glVertex2f(0,0)
        glEnd()

        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)

        A = -2*(d*cos_theta+ xd)*l
        B = -2*(h1 + d*sin_theta- h)*l
        C = k**2-(d*cos_theta+ xd)**2- (h1 + d*sin_theta- h)**2- l**2
        delta = B**2+(A+C)*(A-C)
        t1 = (-B+np.sqrt(delta))/(-A-C)
        self.alpha = np.arctan(t1)*2

        cos_alpha = np.cos(self.alpha)
        sin_alpha = np.sin(self.alpha)

        glBegin(GL_LINES)
        # HB
        glVertex2f(0,h)
        glVertex2f(l*cos_alpha,h+l*sin_alpha)
        # BC
        glVertex2f(l*cos_alpha,h+l*sin_alpha)
        glVertex2f(xd+d*cos_theta,h1+d*sin_theta)
        # CD
        glVertex2f(xd+d*cos_theta,h1+d*sin_theta)
        glVertex2f(xd,h1)
        glEnd()

        glPopMatrix()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        zoom = 0.5

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

    def set_theta(self,value):
        self.theta = value
        self.updateGL()

    def set_alpha(self,value):
        self.alpha = value
        self.updateGL()   
        
class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Ball and Beam")
        self.dc_motor = DC_GlWidget(self)
        
        self.text_theta_la = QtWidgets.QLabel(self)
        self.theta_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.theta_slider.setRange(-180,180)
        self.theta_slider.setValue(0)
        self.text_theta_la.setText(str(self.theta_slider.value()))
        self.theta_slider.valueChanged.connect(self.load_text_value)

        self.load_theta_bt = QtWidgets.QPushButton(text="LOAD THETA")
        self.load_theta_bt.clicked.connect(self.set_theta)

        self.alpha_la = QtWidgets.QLabel(self,text="ALPHA : 0")

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.dc_motor)
        dc_box.addWidget(self.alpha_la)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.theta_slider)
        hbox.addWidget(self.text_theta_la)
        hbox.addWidget(self.load_theta_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        box.addLayout(g_box)

    def load_text_value(self,value):
        self.text_theta_la.setText(str(value))

    def set_theta(self):
        value = self.theta_slider.value()
        alpha = value*np.pi/180
        self.dc_motor.set_theta(alpha)

        connect = 'ALPHA :{:.3}'.format(self.dc_motor.alpha*180/np.pi, 3)
        self.alpha_la.setText(connect)

    # def set_alpha(self):
    #     value = self.theta_slider.value()
    #     self.dc_motor.set_theta(value)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
