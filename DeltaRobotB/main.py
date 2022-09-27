
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *
import delta_robot

class GLWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__()
        self.setMinimumSize(600, 400)

        self.x_ = 0
        self.y_ = 0
        self.z_ = -0.4549
        
        self.delta_robot_B = delta_robot.DeltaRobotB()
        self.delta_robot_B.get_A_B([self.x_, self.y_, self.z_])
        self.postion = self.delta_robot_B.postion

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
        B_P = self.delta_robot_B.get_B_P()
        L_B = self.delta_robot_B.get_A_B([self.x_, self.y_, self.z_])

        self.postion = self.delta_robot_B.postion

        B_P = self.delta_robot_B.get_B_P()
        P_P = self.delta_robot_B.get_P_P()

        h_B = self.delta_robot_B.get_h_B()

        glLineWidth(2)
        self.setupColor("F2C900")
        glBegin(GL_TRIANGLES)
        for i in range(3):
            glVertex3f(*B_P[:,i])
        glEnd()
        glBegin(GL_TRIANGLES)
        for i in range(3):
            glVertex3f(*h_B[:,i])
        glEnd()


        self.setupColor("24ADF3")
        glBegin(GL_TRIANGLES)
        for i in range(3):
            P_P[:,i][0] = P_P[:,i][0] + self.x_
            P_P[:,i][1] = P_P[:,i][1] + self.y_
            P_P[:,i][2] = P_P[:,i][2] + self.z_
            glVertex3f(*P_P[:,i])
        glEnd()

        for i in [0,1,2]:
            self.setupColor("229342")
            glBegin(GL_LINES)
            glVertex3f(*L_B[:,i])
            glVertex3f(*B_P[:,i])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(*h_B[:,i])
            glVertex3f(*B_P[:,i])
            glEnd()

            self.setupColor("E53D30")
            glBegin(GL_LINES)
            glVertex3f(*L_B[:,i])
            glVertex3f(*P_P[:,i])
            glEnd()

        glPopMatrix()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslate(0, 0, -10)
        glTranslate(0, 0.2, 0)
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

class DeltaRobotB(QWidget):
    def __init__(self, *args, **kwargs):
        super(DeltaRobotB, self).__init__()

        self.widget_gl = GLWidget(self)
        self.value_la = QLabel(self)
        self.position_la = QLabel(self)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.widget_gl)
        vbox.addWidget(self.value_la)
        vbox.addWidget(self.position_la)

        print(self.widget_gl.postion[0])

        self.value_la.setText("{:0.3f} {:0.3f} {:0.3f}".format(self.widget_gl.x_, self.widget_gl.y_, self.widget_gl.z_))
        self.position_la.setText("{:0.3f} {:0.3f} {:0.3f}".format(self.widget_gl.postion[0], self.widget_gl.postion[1], self.widget_gl.postion[2]))

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
        self.position_la.setText("{:0.3f} {:0.3f} {:0.3f}".format(self.widget_gl.postion[0], self.widget_gl.postion[1], self.widget_gl.postion[2]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeltaRobotB()
    window.show()
    sys.exit(app.exec_())