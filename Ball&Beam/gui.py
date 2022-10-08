#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
from PyQt5 import QtGui,QtCore,QtWidgets
import pyqtgraph as pg

from PyQt5.QtOpenGL import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# M	mass of the ball	0.11 kg
# R	radius of the ball	0.015 m
# d	lever arm offset	0.03 m
# g	gravitational acceleration	9.8 m/s^2
# L	length of the beam	1.0 m
# J	ball's moment of inertia	9.99e-6 kgm^2
# r	ball position coordinate

_M = 0.11
_R = 0.015
_g = 9.8
_J = 99e-6

_d = 0.1
_L = 1.0
_l = 0.2

_H = 0.2
_xc = 1.0
_yc = 0.0

class InvalidValue(Exception):
    def __init__(self):
        Exception.__init__(self, "Not real solution")

class GlWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.theta = np.pi/3

    def paintGL(self):  
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(0.0, 0.0, 1.0)
        glPushMatrix()

        point_A,alpha = self.get_point_A()
        print(alpha)
        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex2f(0, _H)
        glVertex2f(*point_A)
        glEnd()

        glBegin(GL_LINES)
        glVertex2f(0, 0)
        glVertex2f(0, _H)
        glEnd()

        glBegin(GL_LINES)
        glVertex2f(_xc, _yc)
        glVertex2f(_xc+_d*np.cos(self.theta), _yc+_d*np.sin(self.theta))
        glEnd()

        glBegin(GL_LINES)
        glVertex2f(*point_A)
        glVertex2f(_xc+_d*np.cos(self.theta), _yc+_d*np.sin(self.theta))
        glEnd()
        
        glColor3f(1.0, 0.0, 0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glVertex2f(0, _H)
        glVertex2f(_xc, _yc)
        glVertex2f(*point_A)
        glVertex2f(_xc+_d*np.cos(self.theta), _yc+_d*np.sin(self.theta))
        glEnd()

        glFlush()
        glPopMatrix()


    @staticmethod
    def square_resolution(a, b, c):
        deltal = b ** 2 - 4 * a * c
        if deltal < 0:
            raise InvalidValue()
        x1 = (-b - np.sqrt(deltal)) / (2 * a)
        x2 = (-b + np.sqrt(deltal)) / (2 * a)
        return x1, x2

    def get_point_A(self):
        A = 2*_L*(_xc+_d*np.cos(self.theta))
        B = 2*_L*(_yc+_d*np.sin(self.theta)-_H)
        C = _L**2 - _l**2 + (_xc+_d*np.cos(self.theta))**2+(_yc+_d*np.sin(self.theta)-_H)**2

        t1,t2 = GlWidget.square_resolution(-(A+C),2*B,A-C)
        alpha1 = 2*np.arctan(t1)
        point_A = np.array([_L*np.cos(alpha1),_L*np.sin(alpha1)+_H])
        return point_A,alpha1

    def resizeGL(self, w, h):
        side = min(w, h)
        if side < 0:
            return
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(10.0, w / float(h), 1.0, 20000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -15.0)

    def initializeGL(self):
        pass
    
    def setTheta(self,value):
        self.theta = value*2*np.pi/360
        self.updateGL()

class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.resize(1500, 800)
        self.theta_slider = QtWidgets.QSlider(self)
        self.theta_slider.setRange(-180,180)
        self.theta_slider.valueChanged.connect(self.setTheta)

        self.ball_beam_gl = GlWidget(self)
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.ball_beam_gl)
        hbox.addWidget(self.theta_slider)

    def setTheta(self,value):
        self.ball_beam_gl.setTheta(value)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
