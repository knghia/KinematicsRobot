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

class DC_GlWidget(QGLWidget):
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(400, 400)

        self.U = 0
        self.part_U = 0
        
        self.part_wt = 0
        self.part_thetat = 0

        self.U = 0
        self.delta_U = 0
        self.t = 0
        self.wt = self.func_wt(0)
        self.thetat = self.func_thetat(0)
        self.sign = 1

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

    def func_wt(self,t):
        return K*self.delta_U*(A2*np.exp(x1*t) + A3*np.exp(x2*t) - (A2+A3))

    def func_thetat(self,t):
        return K*self.delta_U*((A2/x1)*np.exp(x1*t) + (A3/x2)*np.exp(x2*t) - (A2+A3)*t - (A2/x1 + A3/x2))

    def drawGL(self):  
        glPushMatrix()
        if self.U - self.part_U != 0:
            self.delta_U = self.U - self.part_U
            self.part_wt = self.wt
            self.part_thetat = self.thetat
            self.part_U = self.U
            self.t = 0
        
        self.wt = self.func_wt(self.t) + self.part_wt
        self.thetat =  self.func_thetat(self.t)+ self.part_wt*self.t
        self.thetat = self.thetat + self.part_thetat

        x = 50*np.cos(self.thetat)
        y = 50*np.sin(self.thetat)

        glBegin(GL_LINES)
        self.setupColor([0xE6, 0x3E, 0x31])
        glVertex2f(x,y)
        glVertex2f(0,0)
        glEnd()

        glPopMatrix()

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

    def setVoltage(self,value):
        self.U = value
        self.updateGL()
        
class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.dc_motor = DC_GlWidget(self)
        
        self.text_value_la = QtWidgets.QLabel(self)
        self.text_value_la.setText("12")
        self.voltage_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.voltage_slider.setRange(-24,24)
        self.voltage_slider.setValue(12)
        self.voltage_slider.valueChanged.connect(self.load_text_value)
        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.set_voltage)

        self.speed_form = GraphicWidget(name="Speed",min= -80, max= 80)
        self.theta_form = GraphicWidget(name="Theta",min= -200, max= 200)

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.dc_motor)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.voltage_slider)
        hbox.addWidget(self.text_value_la)
        hbox.addWidget(self.load_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        g_box.addWidget(self.speed_form)
        g_box.addWidget(self.theta_form)
        box.addLayout(g_box)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_time)
        self.timer.start(100)

    def set_time(self):
        self.dc_motor.set_time()
        self.speed_form.upDateGraphic(self.dc_motor.wt)
        self.theta_form.upDateGraphic(self.dc_motor.thetat)

    def load_text_value(self,value):
        self.text_value_la.setText(str(value))

    def set_voltage(self):
        value = self.voltage_slider.value()
        self.dc_motor.setVoltage(value)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
