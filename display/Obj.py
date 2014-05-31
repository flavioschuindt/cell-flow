from OpenGL.raw.GL.ARB.shader_objects import glUniform1iARB
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
import pygame
from Material import *
from pyglsl import *
from shaders.Shaders import *
from pygame.locals import *
from pygame.constants import *
from loader.objloader import *


class Obj(object):
    def __init__(self):
        # MATERIAL
        self.material = Material()
        self.material.set_shininess(15)
        self.material.set_color(array([1.0, 0.0, 0.0, 1.0]))
        self.material.set_difuse(0.1)
        self.material.set_specular(0.2)
        self.material.enabled = True
        # self.material.set_map_difuse("assets/shaders_offest_offest.jpg")
        # self.material.set_map_bump("assets/shaders_offest_normalmap.jpg")
        # self.material.set_map_displacement("assets/shaders_displacement.png")
        # SHADER
        s = Shaders()
        self.shader_program = compile_program(s.vertex_shader, s.fragment_shader_multi)
        # MODELLING

        pygame.init()
        self.viewport = (800,600)
        # pygame.display.set_mode(self.viewport, OPENGL | DOUBLEBUF)
        # self.srf = pygame.display.set_mode(array([720, 480]), OPENGL | DOUBLEBUF)
        self.obj_model = OBJ("assets/veia.obj")
        self.rotation = 0


    def enable_material(self):
        self.material.enabled = True

    def disable_material(self):
        self.material.enabled = False

    def display(self):
        glUseProgram(self.shader_program)
        # texLoc = glGetUniformLocation(self.shader_program, "Texture0")
        # glUniform1iARB(texLoc, 0)
        # texLoc = glGetUniformLocation(self.shader_program, "Texture1")
        # glUniform1iARB(texLoc, 1)
        # texLoc = glGetUniformLocation(self.shader_program, "Texture2")
        # glUniform1iARB(texLoc, 2)

        # self.material.display()
        glPushMatrix()

        # glTranslate(0.0, -0.1, -1.0)
        glRotate(self.rotation , 1.0, 0.5, 0)
        # glScale(0.6, 0.6, 0.6)

        glCallList(self.obj_model.gl_list)

        # quad = gluNewQuadric()
        # gluQuadricTexture(quad, True)
        # gluSphere(quad, 0.2, 64, 64)
        # gluCylinder(quad, 0.1, 0.1, 0.2, 10, 10)
        # glutSolidCube(0.2)
        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
        # glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
        # glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
        # glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad

        # glEnd()
        glPopMatrix()
        # pygame.display.flip()



__author__ = 'bruno'
