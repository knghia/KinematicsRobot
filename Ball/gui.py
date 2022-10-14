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

class InvalidValue(Exception):
    def __init__(self):
        Exception.__init__(self, "Not real solution")

h = 0.08
h1 = 0.04
l = 0.4
d = 0.04
k = 0.12

class BallBeamGlWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        super(BallBeamGlWidget,self).__init__()

        self.setMinimumSize(400, 400)
        self.t = 0
        self.theta = np.pi/6

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

    def drawGL(self):  
        self.setupColor([0xE6, 0x3E, 0x31])
        # H
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(0,h)
        glVertex2f(0,0)
        glEnd()

        A = -2*(d*np.cos(self.theta)+ l)*l
        B = -2*(d*np.sin(self.theta)- h1)*l
        C = k**2-(d*np.cos(self.theta)+ l)**2- (d*np.sin(self.theta)- h1)**2- l**2
        delta = B**2 - (-A-C)*(A-C)
        t1 = (-B+np.sqrt(delta))/(-A-C)
        t2 = (-B-np.sqrt(delta))/(-A-C)
        alpha = np.arctan(t1)*2

        glBegin(GL_LINES)
        glVertex2f(0,h)
        glVertex2f(l*np.cos(alpha),h+l*np.sin(alpha))

        glVertex2f(l*np.cos(alpha),h+l*np.sin(alpha))
        glVertex2f(l+d*np.cos(self.theta),h1+d*np.sin(self.theta))

        glVertex2f(l+d*np.cos(self.theta),h1+d*np.sin(self.theta))
        glVertex2f(l,h1)
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        xoom = 0.5
        yoom = 0.5
        zoom = 0.5
        glOrtho(-xoom, xoom, -yoom, yoom, -zoom, zoom)
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

    def set_theta(self,value):
        self.theta = value
        self.updateGL()

class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ball_gl = BallBeamGlWidget(self)
        
        self.theta_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.theta_slider.setRange(0,180)
        self.theta_slider.setValue(30)
        self.text_theta = QtWidgets.QLabel(text=str(self.theta_slider.value()))
        
        self.load_bt = QtWidgets.QPushButton(text="LOAD")
        self.load_bt.clicked.connect(self.load_theta)

        box = QtWidgets.QHBoxLayout(self)

        dc_box = QtWidgets.QVBoxLayout()
        dc_box.addWidget(self.ball_gl)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.theta_slider)
        hbox.addWidget(self.text_theta)
        hbox.addWidget(self.load_bt)
        dc_box.addLayout(hbox)

        box.addLayout(dc_box)

        g_box = QtWidgets.QVBoxLayout()
        # g_box.addWidget(self.speed_form)
        # g_box.addWidget(self.theta_form)
        box.addLayout(g_box)

    def set_time(self):
        self.ball_gl.set_time()

    def load_theta(self):
        self.ball_gl.set_theta(self.theta_slider.value()*np.pi/180)
        self.text_theta.setText(str(self.theta_slider.value()))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
