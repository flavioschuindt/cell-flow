from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
from Image import *

class Material(object):
    def __init__(self):
        self.shininess = 0
        self.specular = 1.0
        self.difuse = 1.0
        self.specularRGB = array([1.0, 1.0, 1.0, 1.0])
        self.difuseRGB = array([1.0, 1.0, 1.0, 1.0])
        # self.set_difuse(0.1)
        self.enabled = True
        self.texture = Texture()
    def set_shininess(self,v):
        self.shininess = max(0.0, min(128.0, v))
        print "SHININESS ->" +  str(self.shininess)

    def set_specular(self, v):
        self.specular = max(0.0, min(1.0, v))
        print "SPECULAR ->" +  str(self.specular)

    def set_difuse(self, v):
        self.difuse = max(0.0, min(1.0, v))
        print "DIFUSE ->" + str(self.difuse)

    def set_map_difuse(self, name):
        self.texture.loadTextures( self.texture.DIFUSE, name)

    def set_map_bump(self, name):
        self.texture.loadTextures( self.texture.BUMP, name)

    def display(self):
        # Aplica caracteristicas do material ao objeto
        difusePass = self.difuseRGB * self.difuse
        difusePass[3] = 1.0 # Corrige o alpha
        specularPass = self.specularRGB * self.specular
        specularPass[3] = 1.0 # Corrige o alpha

        if self.enabled:
            glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, difusePass)
            glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specularPass)
            glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)

class Texture(object):
    def __init__(self):
        self.DIFUSE = 0
        self.BUMP = 1
        glEnable(GL_TEXTURE_2D)
        self.difuseMap = []
        self.bumpMap = []
        # self.loadTextures("Wall.bmp")
        # self.difuseMap = self.loadTextures("Wall_bump.png")

    def loadTextures(self, channel , pathFile):
        image = open(pathFile)
        ix = image.size[0]
        iy = image.size[1]
        image = image.convert("RGBA").tostring("raw", "RGBA", 0, -1)

        # Create Texture
        if channel == self.DIFUSE:
            self.difuseMap = glGenTextures(1)
        elif channel == self.BUMP:
            self.bumpMap = glGenTextures(1)
        # glBindTexture(GL_TEXTURE_2D, int(texture))   # 2d texture (x and y size)

        # Create MipMapped Texture
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)

__author__ = 'bruno'
