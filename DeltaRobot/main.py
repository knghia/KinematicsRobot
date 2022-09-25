
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

        self.alpha = 0
        self.beta = 0
        self.gama = 0

        self.xRot = -2500
        self.yRot = 2000
        self.zRot = 0.0

        self.z_zoom = 35
        self.xTran = 0
        self.yTran = 0

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
        glBegin(GL_LINES)
        # X axis
        self.setupColor([255,0,0])
        glVertex3f(150,0,0)
        glVertex3f(0,0,0)

        # Y axis
        self.setupColor([0,255,0])
        glVertex3f(0,150,0)
        glVertex3f(0,0,0)

        # Z axis
        self.setupColor([0,0,255])
        glVertex3f(0,0,150)
        glVertex3f(0,0,0)
        glEnd()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslate(0, 0, self.z_zoom)
        glRotated(self.xRot/16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot/16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot/16.0, 0.0, 0.0, 1.0)
        glRotated(+90.0, 1.0, 0.0, 0.0)
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
        glTranslated(0.0, 0.0, -400.0)

    def setupColor(self, color):
        color[0] = color[0]/255
        color[1] = color[1]/255
        color[2] = color[2]/255
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

    # def setAlpha(self, alpha):
    #     self.alpha = alpha*np.pi/180
    #     self.updateGL()

    # def setBeta(self, beta):
    #     self.beta = beta*np.pi/180
    #     self.updateGL()

    # def setGama(self, gama):
    #     self.gama = gama*np.pi/180
    #     self.updateGL()

class LINK3_2D(QWidget):
    def __init__(self, *args, **kwargs):
        super(LINK3_2D, self).__init__()

        self.widget_gl = GLWidget(self)

        # self.alpha_slider = QSlider(Qt.Horizontal)
        # self.alpha_slider.setRange(0,720)
        # self.alpha_slider.valueChanged.connect(self.change_alpha_value)

        # self.beta_slider = QSlider(Qt.Horizontal)
        # self.beta_slider.setRange(0,720)
        # self.beta_slider.valueChanged.connect(self.change_beta_value)

        # self.gama_slider = QSlider(Qt.Horizontal)
        # self.gama_slider.setRange(0,720)
        # self.gama_slider.valueChanged.connect(self.change_gama_value)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.widget_gl)
        # vbox.addWidget(self.alpha_slider)
        # vbox.addWidget(self.beta_slider)
        # vbox.addWidget(self.gama_slider)

    def keyPressEvent(self, event):
        print(event.key())
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_W:
                self.widget_gl.z_zoom +=100
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_S:
                self.widget_gl.z_zoom -=100
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Down:
                self.widget_gl.yRot += 100
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Up:
                self.widget_gl.yRot -= 100
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Left:
                self.widget_gl.zRot += 100
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Right:
                self.widget_gl.zRot -= 100
                self.widget_gl.updateGL()



    # def change_alpha_value(self,value):
    #     self.widget_gl.setAlpha(value)
    
    # def change_beta_value(self,value):
    #     self.widget_gl.setBeta(value)

    # def change_gama_value(self,value):
    #     self.widget_gl.setGama(value)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LINK3_2D()
    window.show()
    sys.exit(app.exec_())