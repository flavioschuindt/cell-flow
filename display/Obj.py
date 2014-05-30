from OpenGL.raw.GL.ARB.shader_objects import glUniform1iARB
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
from Material import *
from pyglsl import *
from shaders.Shaders import *

class Obj(object):
    def __init__(self):
        self.material = Material()
        self.material.set_shininess(15)
        self.material.set_color(array([1.0, 1.0, 0.0, 1.0]))
        self.material.set_difuse(0.1)
        self.material.set_specular(0.2)
        self.material.enabled = True
        self.material.set_map_difuse("shaders_offest_offest.jpg")
        # self.material.set_map_difuse("shaders_offest_normalmap.jpg")
        self.material.set_map_bump("shaders_offest_normalmap.jpg")

        global s
        s = Shaders()

        global program
        program = compile_program(s.vertex_shader, s.fragment_shader_multi)



    def enable_material(self):
        self.material.enabled = True

    def disable_material(self):
        self.material.enabled = False

    def display(self):
        global program
        glUseProgram(program)
        texLoc = glGetUniformLocation(program, "Texture0")
        glUniform1iARB(texLoc, 0)
        texLoc = glGetUniformLocation(program, "Texture1")
        glUniform1iARB(texLoc, 1)
        self.material.display()
        glPushMatrix()
        # glTranslate(0.0, -0.1, -1.0)
        # glRotate(-120 , 1.0, 1.0, 0)
        # glScale(0.6, 0.6, 0.6)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, True)
        gluSphere(quad, 0.2, 36, 36)
        # gluCylinder(quad, 0.1, 0.1, 0.2, 10, 10)
        # glutSolidCube(0.2)

        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        # glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        # glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
        # glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad

        # glEnd()
        glPopMatrix()



__author__ = 'bruno'
