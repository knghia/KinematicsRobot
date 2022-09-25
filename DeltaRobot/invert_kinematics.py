
from math import cos
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtOpenGL import *

class GLWidget(QGLWidget):

    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__()
        self.setMinimumSize(600, 400)

        self._xB = 200
        self._yB = 0

        self.alpha = 0
        self.beta = 0

        self.a = 100
        self.b = 100

    def setColor(self, color):
        color[0] = color[0]/255
        color[1] = color[1]/255
        color[2] = color[2]/255
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

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
        
        print(self._xB,self._yB)

        if self._xB == 0:
            if self._yB >= 0:
                delta = np.pi/2
            else:
                delta = -np.pi/2
        else:
            if (self._xB > 0 ) and (self._yB >= 0):
                delta = np.arctan(self._yB/self._xB)
            elif (self._xB < 0 ) and (self._yB > 0):
                delta = np.arctan(self._yB/self._xB) + np.pi
            elif (self._xB < 0 ) and (self._yB <= 0):
                delta = np.arctan(self._yB/self._xB) + np.pi
            elif (self._xB > 0 ) and (self._yB <= 0):
                delta = np.arctan(self._yB/self._xB) + 2*np.pi    

        d = np.sqrt(self._xB**2 + self._yB**2)

        cos_beta = (d**2 - self.a**2 - self.b**2)/(2*self.a*self.b)
        self.beta = np.arccos(cos_beta)

        sin_beta = np.sqrt(1-cos_beta**2)
        if cos_beta == -1:
            self.alpha = delta
        else:
            self.alpha = delta - np.arcsin(self.b*sin_beta/d)
        
        print(self.alpha*180/np.pi, delta*180/np.pi)

        glLineWidth(3.0)
        glBegin(GL_LINES)
        self.setColor([255, 255, 0])
        R_A = np.array([
            [np.cos(self.alpha), -np.sin(self.alpha) , 0],
            [np.sin(self.alpha), np.cos(self.alpha) , 0],
            [0, 0 , 1]])

        T_A = np.array([[1, 0, self.a], [0, 1, 0], [0, 0, 1]])
        __X = np.dot(R_A,T_A)
        xA, yA = __X[0][2],__X[1][2]

        glVertex2f(0,0)
        glVertex2f(xA,yA)

        self.setColor([0, 255, 255])
        R_B = np.array([
            [np.cos(self.beta), -np.sin(self.beta) , 0],
            [np.sin(self.beta), np.cos(self.beta) , 0],
            [0, 0 , 1]])
        T_B = np.array([[1, 0, self.b], [0, 1, 0], [0, 0, 1]])

        __X = np.dot(__X, R_B)
        __X = np.dot(__X, T_B)

        xB, yB = __X[0][2], __X[1][2]

        glVertex2f(xA, yA)
        glVertex2f(xB, yB)
        glEnd()

        self.setColor([255, 0, 0])
        self.drawCircle(0,0,self.a+self.b)

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

    def drawGrid(self):
        glPushMatrix()
        glLineWidth(2)
        self.setColor([8, 108, 162])
        step = 0.05
        num = 10
        for i in range(-num, num+1):
            glBegin(GL_LINES)
            glVertex3f(i*step, -num * step, 0)
            glVertex3f(i*step, num*step, 0)
            glVertex3f(-num * step, i*step, 0)
            glVertex3f(num*step, i*step, 0)
            glEnd()
        glPopMatrix()
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

    def setX(self, X):
        self._xB = X
        self.updateGL()

    def setY(self, Y):
        self._yB = Y
        self.updateGL()

class LINK3_2D(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__()

        self.widget_gl = GLWidget(self)

        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setRange(-200,200)
        self.x_slider.setValue(200)
        self.x_slider.valueChanged.connect(self.change_x_value)

        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setRange(-200,200)
        self.y_slider.setValue(0)
        self.y_slider.valueChanged.connect(self.change_y_value)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.widget_gl)
        vbox.addWidget(self.x_slider)
        vbox.addWidget(self.y_slider)

    def change_x_value(self,value):
        self.widget_gl.setX(value)
    
    def change_y_value(self,value):
        self.widget_gl.setY(value)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LINK3_2D()
    window.show()
    sys.exit(app.exec_())