from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
from PIL import Image
import numpy as np


class Material(object):
    def __init__(self):
        self.shininess = 0
        self.specular = 1.0
        self.difuse = 1.0
        self.specularRGB = np.array([1.0, 1.0, 1.0, 1.0])
        self.difuseRGB = np.array([1.0, 1.0, 1.0, 1.0])
        # self.set_difuse(0.1)
        self.enabled = True
        self.texture = Texture()

    def set_color(self,v):
        self.difuseRGB = v

    def set_shininess(self,v):
        self.shininess = max(0.0, min(128.0, v))
        print "SHININESS ->" + str(self.shininess)

    def set_specular(self, v):
        self.specular = max(0.0, min(1.0, v))
        print "SPECULAR ->" + str(self.specular)

    def set_difuse(self, v):
        self.difuse = max(0.0, min(1.0, v))
        print "DIFUSE ->" + str(self.difuse)

    def set_map_difuse(self, name):
        glActiveTexture(GL_TEXTURE0)
        self.texture.difuse_map = self.texture.loadTextures(name)

    def set_map_bump(self, name):
        glActiveTexture(GL_TEXTURE1)
        self.texture.bump_map = self.texture.loadTextures(name)

    def set_map_displacement(self, name):
        glActiveTexture(GL_TEXTURE2)
        self.texture.displacement = self.texture.loadTextures(name)

    def display(self):
        # Aplica caracteristicas do material ao objeto
        # difusePass = self.difuseRGB * self.difuse
        difusePass = [0,0,0,0]
        difusePass[0] = self.difuseRGB[0] * self.difuse
        difusePass[1] = self.difuseRGB[1] * self.difuse
        difusePass[2] = self.difuseRGB[2] * self.difuse
        difusePass[3] = 1.0
        # difusePass[3] = 1.0 # Corrige o alpha
        # specularPass = self.specularRGB * self.specular
        # specularPass[3] = 1.0 # Corrige o alpha
        #
        specularPass = [0, 0, 0, 0]
        specularPass[0] = self.specularRGB[0] * self.specular
        specularPass[1] = self.specularRGB[1] * self.specular
        specularPass[2] = self.specularRGB[2] * self.specular
        specularPass[3] = 1.0

        if self.enabled:
            glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, difusePass)
            glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specularPass)
            glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)

class Texture(object):
    def __init__(self):
        self.difuse_map = []
        self.bump_map = []
        self.displacement = []
        # self.loadTextures("Wall.bmp")
        # self.difuseMap = self.loadTextures("Wall_bump.png")

    def loadTextures(self, pathFile):
        "Loads an image from a file as a texture"
        # Read file and get pixels
        imagefile = Image.open(pathFile)
        sx,sy = imagefile.size[0:2]
        global pixels
        pixels = imagefile.convert("RGBA").tostring("raw", "RGBA", 0, -1)

        # Create an OpenGL texture name and load image into it
        image = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D,  image)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, sx, sy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
        gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, sx, sy, GL_RGBA, GL_UNSIGNED_BYTE, pixels)

        # How mix with light
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # How to Wrap
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # How to filter MAG and MIN
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        # Return texture name (an integer)
        return image


__author__ = 'bruno'
