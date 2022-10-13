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

# Ra = 2
# La = 0.23
# Jm = 0.000052
# Bm = 0.01
# Kt = 0.235
# Ke = 0.235

# a = 1
# b = (Jm*Ra + La*Bm)/(La*Jm)
# c = (Ke*Kt + Ra*Bm)/(La*Jm)

# delta = b**2 - 4*a*c
# x1 = (-b+np.sqrt(delta))/(2*a)
# x2 = (-b-np.sqrt(delta))/(2*a)
# K = Kt/(La*Jm)
# A1 = 1/(x1*x2)
# A2 = 1/(x1*(x1-x2))
# A3 = 1/(x2*(x2-x1))

class GraphicWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None, *args, **kwargs):
        super(GraphicWidget, self).__init__()

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

class BallGlWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        super(BallGlWidget,self).__init__()

        self.setMinimumSize(400, 400)
        self.t = 0
        self.alpha = np.pi/6

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

    def drawGL(self):  
        x = 50*np.cos(self.alpha)
        y = 50*np.sin(self.alpha)
        self.setupColor([0xE6, 0x3E, 0x31])
        glBegin(GL_LINES)
        glVertex2f(x,y)
        glVertex2f(0,0)
        glVertex2f(0,0)
        glVertex2f(-200,0)
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-100.0, 100.0, -100.0, 100.0, -100.0, 100.0)
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

    def set_time(self):
        self.t += 0.01
        self.updateGL()

    def set_alpha(self,value):
        self.alpha = value
        self.updateGL()

class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ball_gl = BallGlWidget(self)
        
        self.alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.alpha_slider.setRange(0,180)
        self.alpha_slider.setValue(60)
        self.alpha_slider.valueChanged.connect(self.load_alpha_text)
        self.text_alpha = QtWidgets.QLabel(text=str(self.alpha_slider.value()))

        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.start_simulation)

        self.speed_form = GraphicWidget(name="Speed",min= -80, max= 80)
        self.theta_form = GraphicWidget(name="Theta",min= -200, max= 200)

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.ball_gl)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.alpha_slider)
        hbox.addWidget(self.text_alpha)
        hbox.addWidget(self.load_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        g_box.addWidget(self.speed_form)
        g_box.addWidget(self.theta_form)
        box.addLayout(g_box)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_time)
        
    def start_simulation(self):
        self.timer.start(100)

    def set_time(self):
        self.ball_gl.set_time()

    def load_alpha_text(self,value):
        self.ball_gl.set_alpha(value*np.pi/180)
        self.text_alpha.setText(str(value))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
