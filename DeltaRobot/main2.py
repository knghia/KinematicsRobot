
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *
import delta

class GLWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__()
        self.setMinimumSize(600, 400)

        self.x_ = 0
        self.y_ = 0
        self.z_ = -0.283
        self.delta_robot = delta.DeltaRobot()

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

        glClearColor(193.0/255, 193.0/255, 193.0/255, 1.0)

    def drawGL(self):
        glPushMatrix()
        
        try:
            self.delta_robot.Position = np.array([self.x_, self.y_, self.z_])
        except delta.InvalidValue:
            QMessageBox.warning(self,"","Error")
            self.x_ = 0
            self.y_ = 0
            self.z_ = -0.283
            self.delta_robot.Position = np.array([0, 0, -0.283])
        
        position = self.delta_robot.Position

        B = self.delta_robot.get_B_B()
        b = self.delta_robot.get_B_b()
        P = self.delta_robot.get_P_P()
        A = self.delta_robot.get_vector_B_A()

        position = self.delta_robot.Position
        base_P = P
        base_P[:, 0] += position
        base_P[:, 1] += position
        base_P[:, 2] += position

        self.setupColor("0000F6")

        glLineWidth(2)
        glBegin(GL_TRIANGLES)
        for i in range(3):
            glVertex3f(*P[:,i])
        glEnd()

        self.setupColor("FCC526")

        glColor3f(1,1,1)
        for i in [0,2]:
            glBegin(GL_LINES)
            glVertex3f(*B[:,i])
            glVertex3f(*A[:,i])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(*B[:,i])
            glVertex3f(*A[:,i])
            glEnd()
        
            glBegin(GL_LINES)
            glVertex3f(*P[:,i])
            glVertex3f(*A[:,i])
            glEnd()

        average = lambda array: np.array([sum(array[0]) / 3, sum(array[1]) / 3, sum(array[2]) / 3]).T
        cb_P = average(base_P)

        glBegin(GL_LINES)
        glVertex3f(0,0,0)
        glVertex3f(*cb_P)
        glEnd()

        glBegin(GL_TRIANGLES)
        for i in range(3):
            glVertex3f(*b[:,i])
        glEnd()

        for i in [1]:
            glBegin(GL_LINES)
            glVertex3f(*B[:,i])
            glVertex3f(*A[:,i])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(*B[:,i])
            glVertex3f(*A[:,i])
            glEnd()
        
            glBegin(GL_LINES)
            glVertex3f(*P[:,i])
            glVertex3f(*A[:,i])
            glEnd()

        glFlush()

        glPopMatrix()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslate(0, 0, -1)
        glRotated(-2500/16.0, 1.0, 0.0, 0.0)
        glRotated(2000/16.0, 0.0, 1.0, 0.0)
        glRotated(0.0/16.0, 0.0, 0.0, 1.0)
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
        gluPerspective(1.0, w / float(h), 1.0, 20000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def setupColor(self, color):
        color = self.hex_to_rgb(color)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)

    def hex_to_rgb(self, hex):
        return list(int(hex[i:i+2], 16)/255 for i in (0, 2, 4)) 

class DeltaRobot(QWidget):
    def __init__(self, *args, **kwargs):
        super(DeltaRobot, self).__init__()

        self.widget_gl = GLWidget(self)
        self.value_la = QLabel(self)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.widget_gl)
        vbox.addWidget(self.value_la)

        self.value_la.setText("{:0.3f} {:0.3f} {:0.3f}".format(self.widget_gl.x_, self.widget_gl.y_, self.widget_gl.z_))

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_W:
                self.widget_gl.z_ += 0.01
                self.widget_gl.updateGL()
                
            elif event.key() == Qt.Key_S:
                self.widget_gl.z_ -= 0.01
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Down:
                self.widget_gl.y_ += 0.01
                self.widget_gl.updateGL()
            
            elif event.key() == Qt.Key_Up:
                self.widget_gl.y_ -= 0.01
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Left:
                self.widget_gl.x_ += 0.01
                self.widget_gl.updateGL()

            elif event.key() == Qt.Key_Right:
                self.widget_gl.x_ -= 0.01
                self.widget_gl.updateGL()

        self.value_la.setText("{:0.3f} {:0.3f} {:0.3f}".format(self.widget_gl.x_, self.widget_gl.y_, self.widget_gl.z_))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeltaRobot()
    window.show()
    sys.exit(app.exec_())