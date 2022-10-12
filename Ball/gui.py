#!/usr/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtOpenGL,QtWidgets

RED_COLOR = [255, 92, 92]
GREEN_COLOR = [57, 217, 138]
BLUE_COLOR = [91, 141, 236]
ORANGE_COLOR = [253, 172, 66]
YELLOW_COLOR = [255,255,51]
PURPLE_COLOR = [75,0,130]
MAROON_COLOR = [222,184,135]
WHITE_COLOR = [255,255,255]

class InvalidValue(Exception):
    def __init__(self):
        Exception.__init__(self, "Not real solution")

class GLWidget(QtOpenGL.QGLWidget):

    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__()
        
        self.g = 9.8
        self._L = 1000
        self._angle = np.pi/6
        self._sin_alpha = np.sin(self._angle)
        self._cos_alpha = np.cos(self._angle)
        self._tan_alpha = self._sin_alpha/self._cos_alpha

        self._r_Ball = 100
        self._m_Ball = 100
        self._mu  = 0.01

        self._v_L = [self._L*self._cos_alpha, self._L*self._sin_alpha]
        self._v_Lu = [self._v_L[0]- self._r_Ball*self._sin_alpha, self._v_L[1]+ self._r_Ball*self._cos_alpha]
        self._v_Ou = [self._r_Ball*(1-1/self._cos_alpha)/self._tan_alpha, self._r_Ball]
        self._Q = [-2000 , 0]
        self._Qu = [-2000 , self._r_Ball]

        self._status = 1
        self._t = 0

        self.tau = (5/7)*self.g*(self._sin_alpha-self._mu*self._cos_alpha)

        A = 1
        B = (5/7)*self.g*self._mu
        C = 0
        self._alpha, self._beta = GLWidget.square_resolution_complex(A,B,C)
        D = self._beta - self._alpha
        D1 = self._L*self._beta - np.sqrt(2*self.tau*self._L)
        D2 =  np.sqrt(2*self.tau*self._L) - self._alpha*self._L

        self._C1 = D1/D
        self._C2 = D2/D

        self.position = 0
        self.velocity = 0

        self.setMinimumSize(800,400)

    @staticmethod
    def square_resolution_complex(a, b, c):
        deltal = b ** 2 - 4 * a * c
        if deltal >= 0:
            k1 = (-b+np.sqrt(deltal))/(2*a)
            k2 = (-b-np.sqrt(deltal))/(2*a)
            return k1,k2
        else:
            alpha = -b/(2*a)
            beta = np.sqrt(np.abs(deltal))/(2*a)
            return alpha,beta

    def drawGL(self):
        self.setupColor(RED_COLOR)
        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(0, 0)
        glVertex2f(*self._v_L)
        glVertex2f(0, 0)
        glVertex2f(*self._Q)
        glEnd()

        if self._t < np.sqrt(2*self._L/self.tau):
            self.position = self.tau/2*self._t**2
            self.velocity = self.tau*self._t
            _xB = self.position
            _xH = (self._L - _xB - self._r_Ball*self._tan_alpha)*self._cos_alpha
            _yH = _xH*self._tan_alpha + self._r_Ball/self._cos_alpha
            self.drawCircle(_xH,_yH,self._r_Ball)

        else:
            _t =self._t- np.sqrt(2*self._L/self.tau)
            self.position = self._C1*np.e**(self._alpha*_t)+self._C2*np.e**(self._beta*_t)
            self.velocity = self._alpha*self._C1*np.e**(self._alpha*_t)+ self._beta*self._C2*np.e**(self._beta*_t)
            _xB = self._L-self.position
            self.drawCircle(_xB,self._r_Ball,self._r_Ball)


    def drawPoints(self,xc,yc,x,y):
        glLineWidth(5)
        glBegin(GL_POINTS)
        glVertex2f(xc+x, yc+y)
        glVertex2f(xc-x, yc+y)
        glVertex2f(xc+x, yc-y)
        glVertex2f(xc-x, yc-y)
 
        glVertex2f(xc+y, yc+x)
        glVertex2f(xc-y, yc+x)
        glVertex2f(xc+y, yc-x)
        glVertex2f(xc-y, yc-x)
        glEnd()
        
    def drawCircle(self,xc,yc,r):
        x = 0
        y = r
        d = 3 - 2 * r
        self.drawPoints(xc, yc, x, y)
        while(x<=y):
            x+=1
            if (d > 0):
                y-=1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            self.drawPoints(xc, yc, x, y)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self.drawGL()
        glPopMatrix()

 
    def initializeGL(self):
        glClearColor(0, 0, 0, 1.0)
        glColor3f(1,0,0)
        glOrtho(-500,500,500,-500,0,0.5)

    def resizeGL(self, width, height):
        if (height != 0):
            side = min(width, height)
            if side < 0:
                return
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(35.0, width / float(height), 1.0, 20000.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslated(0.0, 0.0, -5000.0)

    def setupColor(self, color):
        color = [element/255.0 for element in color]
        glColor3f(*color)

    def uploadValue(self, value):
        self._t+=value
        self.updateGL()
        return self.position,self.velocity

class GraphicWidget(QtWidgets.QGroupBox):

    def __init__(self, parent=None, *args, **kwargs):

        super().__init__(parent)

        self.numberOfSamples = 2000

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

class BallMove(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(BallMove, self).__init__()

        self.gl_widget = GLWidget()

        self.action = QtWidgets.QCheckBox(text="Reload")
        self.action.stateChanged.connect(self.action_timer)

        self.position_gl = GraphicWidget(name="POSITION",min=0, max= 3000)
        self.velocity_gl = GraphicWidget(name="Velocity",min=-200, max= 200)

        velocity_gl = QtWidgets.QVBoxLayout(self)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.gl_widget)
        hbox.addWidget(self.action)

        velocity_gl.addLayout(hbox)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.position_gl)
        hbox.addWidget(self.velocity_gl)

        velocity_gl.addLayout(hbox)

        self.timer= QtCore.QTimer(self)
        self.timer.timeout.connect(self.upload_t)

    def action_timer(self):
        if self.action.isChecked():
            print("Start")
            self.startTimer()
        else:
            self.endTimer()

    def upload_t(self):
        p,v = self.gl_widget.uploadValue(0.04)
        self.position_gl.upDateGraphic(p)
        self.velocity_gl.upDateGraphic(v)

    def startTimer(self):
        self.timer.start(10)

    def endTimer(self):
        self.timer.stop()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = BallMove()
    mainWindow.show()
    sys.exit(app.exec_())
