
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtOpenGL import *


Ra = 2.32
La = 0.238*10e-3
Jm = 10.8*10e-7
Bm = 0.0
Kt = 2.85*10e-3
Ke = 1/(408*0.10472)

_A = La*Jm/Kt
_B = (Jm*Ra + La*Bm)/Kt
_C = (Ke*Kt + Ra*Bm)/Kt
Delta = _B**2 - 4*_A*_C
print("Delta ",Delta)
alpha = (-_B + math.sqrt(Delta))/(2*_A)
beta = (-_B - math.sqrt(Delta))/(2*_A)

class GLWidget(QGLWidget):

    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__()
        self.setMinimumSize(600, 400)

        self.Uin = 0
        self.time = 0
        self.theta = 0

    def setColor(self, color):
        color[0] = color[0]/255
        color[1] = color[1]/255
        color[2] = color[2]/255
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

    def square_2(self, a, b, c):
        deltal = b ** 2 - 4 * a * c
        if deltal >= 0:
            k1 = (-b+np.sqrt(deltal))/(2*a)
            k2 = (-b-np.sqrt(deltal))/(2*a)
            return k1,k2
        else:
            raise "Error"

    def initializeGL(self):
        ambientLight = [0.7, 0.7, 0.7, 1.0]
        diffuseLight = [0.7, 0.8, 0.8, 1.0]
        specularLight = [0.4, 0.4, 0.4, 1.0]
        positionLight = [20.0, 20.0, 20.0, 0.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight)
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1.0)
        glLightfv(GL_LIGHT0, GL_POSITION, positionLight)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glClearColor(178.0/255, 213.0/255, 214.0/255, 1.0)

    def drawGL(self):
        self.setColor([255, 0, 0])
        self.drawCircle(0,0,100)

        t = self.time
        _C1 = -alpha*((self.Uin/_C)/(alpha - beta))
        _C2 = beta*((self.Uin/_C)/(alpha - beta))
        self.theta = (_C1/alpha)*math.e**(alpha*t)+ (_C2/beta)*math.e**(beta*t) + (self.Uin/_C)*t

        x = 100*math.cos(self.theta)
        y = 100*math.sin(self.theta)

        if x == 0:
            if (y>0):
                glLineWidth(1)
                glBegin(GL_LINES)
                glVertex2f(x,y)
                glVertex2f(x,y-5)
                glEnd()
            else:
                glLineWidth(1)
                glBegin(GL_LINES)
                glVertex2f(x,y)
                glVertex2f(x,y+5)
                glEnd()
        else:
            k = y/x
            a = 1 + k**2
            b = -2*(x+k*y)
            c = x**2 + y**2 - 10**2
            k1, k2 = self.square_2(a,b,c)

            if x>=0:
                glLineWidth(1)
                glBegin(GL_LINES)
                glVertex2f(k2, k*k2)
                glVertex2f(x,y)
                glEnd()
            else:
                glLineWidth(1)
                glBegin(GL_LINES)
                glVertex2f(k1, k*k1)
                glVertex2f(x,y)
                glEnd()    

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        self.drawGL()
        glPopMatrix()

    def resizeGL(self, w, h):
        side = min(w, h)
        if side < 0:
            return
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100.0, w / float(h), 1.0, 20000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -200.0)

    def drawPoints(self,xc,yc,x,y):
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

    def load_time(self,value):
        self.time += value
        self.updateGL()

    def load_voltage(self,value):
        self.Uin = value
        self.updateGL()

    def get_theta(self):
        return self.theta

class LINK3_2D(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__()

        self.widget_gl = GLWidget(self)

        self.voltage = QSlider(Qt.Horizontal)
        self.voltage.setRange(-24,24)
        self.voltage.valueChanged.connect(self.change_voltage)

        self.theta_la = QLabel(text="0")

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.widget_gl)
        vbox.addWidget(self.voltage)
        vbox.addWidget(self.theta_la)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_time)
        self.timer.start(100)

    def change_voltage(self,value):
        self.widget_gl.load_voltage(value)

    def load_time(self):
        self.widget_gl.load_time(100/1000)
        self.theta_la.setText(str(self.widget_gl.get_theta()))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LINK3_2D()
    window.show()
    sys.exit(app.exec_())