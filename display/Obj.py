from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
from Material import *

class Obj(object):
    def __init__(self):
        self.material = Material()
        self.material.set_shininess(15)
        self.material.set_difuse(0.1)
        self.material.set_specular(0.42)
        self.material.enabled = True
        # self.material.set_map_difuse("Wall.bmp")
        self.material.set_map_difuse("shaders_offest_normalmap.jpg")
        # self.material.set_map_bump("shaders_offest_normalmap.jpg")
        print

    def enable_material(self):
        self.material.enabled = True

    def disable_material(self):
        self.material.enabled = False

    def display(self):
        self.material.display()
        glPushMatrix()

        # glTranslate(0.0, -0.1, -1.0)
        glRotate(60 , 1.0, 0.0, 0)
        # glScale(0.6, 0.6, 0.6)

        quad = gluNewQuadric()
        gluQuadricTexture(quad, True)
        gluSphere(quad, 0.2, 36, 36)
        # gluCylinder(quad, 0.1, 0.1, 0.2, 10, 10)

        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        # glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        # glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
        # glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
        #
        # glEnd()
        glPopMatrix()



__author__ = 'bruno'
