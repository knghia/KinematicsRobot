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
d = 0.06
l = 0.4
k = 0.12
xd = 0.4 - d
yd = 0

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

        cos_alpha = np.cos(self.alpha)
        sin_alpha = np.sin(self.alpha)

        A = 2*(xd - l*cos_alpha)*d
        B = 2*(yd - h - l*sin_alpha)*d
        C = k**2-(xd - l*cos_alpha)**2- (yd - h - l*sin_alpha)**2- d**2
        
        delta = B**2+(A+C)*(A-C)
        t1 = (-B-np.sqrt(delta))/(-A-C)
        self.theta = np.arctan(t1)*2

        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)

        glBegin(GL_LINES)
        # HB
        glVertex2f(0,h)
        glVertex2f(l*cos_alpha,h+l*sin_alpha)
        # BC
        glVertex2f(l*cos_alpha,h+l*sin_alpha)
        glVertex2f(xd+d*cos_theta,yd+d*sin_theta)
        # CD
        glVertex2f(xd+d*cos_theta,yd+d*sin_theta)
        glVertex2f(xd,yd)
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

    def setupColor(self, color):
        color[0] = color[0]/255
        color[1] = color[1]/255
        color[2] = color[2]/255
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

    def set_alpha(self,value):
        self.alpha = value
        self.updateGL()   
        
class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Ball and Beam")
        self.dc_motor = DC_GlWidget(self)
        
        self.text_alpha_la = QtWidgets.QLabel(self)
        self.alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.alpha_slider.setRange(-10,10)
        self.alpha_slider.setValue(0)
        self.text_alpha_la.setText(str(self.alpha_slider.value()))
        self.alpha_slider.valueChanged.connect(self.load_text_value)

        self.load_alpha_bt = QtWidgets.QPushButton(text="LOAD THETA")
        self.load_alpha_bt.clicked.connect(self.set_alpha)

        self.theta_la = QtWidgets.QLabel(self,text="Theta : 0")

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.dc_motor)
        dc_box.addWidget(self.theta_la)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.alpha_slider)
        hbox.addWidget(self.text_alpha_la)
        hbox.addWidget(self.load_alpha_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        box.addLayout(g_box)

    def load_text_value(self,value):
        self.text_alpha_la.setText(str(value))

    def set_alpha(self):
        value = self.alpha_slider.value()
        alpha = value*np.pi/180
        self.dc_motor.set_alpha(alpha)
        connect = 'Theta :{:.3}'.format(self.dc_motor.theta*180/np.pi, 3)
        self.theta_la.setText(connect)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
