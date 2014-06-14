from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from const import FRAME_PERIOD, INIT_WINDOW_SIZE, INIT_WINDOW_POSITION, \
    BACKGROUND_COLOR, TORUS_SIDES, TORUS_RINGS, TORUS_COLOR, \
    TORUS_INNER_RADIUS, TORUS_OUTTER_RADIUS, TORUS_MASS_RANGE, \
    TORUS_QUANTITY, FOVY, Z_NEAR, Z_FAR, FLUID_FORCE, GRAVITY_FORCE_FACTOR, \
    TORUS_DESIRED_SEPARATION, TORUS_FLOCKING_MAX_SPEED, TORUS_FLOCKING_MAX_FORCE, \
    GRID_CELL_QUANTITY
from math import tan, radians
from numpy import array
from display.GenericObj import *
from display.ObjManager import *

viewport = None
far_z = 0
current_w, current_h = INIT_WINDOW_SIZE
artery = None
blood = None

def reshape(w, h):
    global current_w, current_h, blood
    current_w = w
    current_h = h

    ar = float(w)/h
    l_y = round(tan(radians(FOVY/2))*blood.far_z, 2) * 2
    l_x = round(ar * l_y, 2) * 2

    blood.recreate_grid(l_x=l_x, l_y=l_y, cell_quantity=GRID_CELL_QUANTITY)

    glViewport(0, 0, current_w, current_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, ar, Z_NEAR, Z_FAR)
    glMatrixMode(GL_MODELVIEW)

def display():
    global current_w, current_h, artery, blood
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glTranslate(0, 0, -2)
    # glutSolidSphere(0.5, 16,16)
    # glCallList(artery.model.gl_list)
    artery.display()
    blood.update()
    blood.display()
    pygame.display.flip()

def create_scene():
    global artery, blood

    w, h = INIT_WINDOW_SIZE
    glViewport(0, 0, current_w, current_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, float(w)/h, Z_NEAR, Z_FAR)
    glMatrixMode(GL_MODELVIEW)

    artery = GenericObj(1.0, "veia.obj")
    # artery.material.difuseRGB =[0.0, 0.0, 0.0,0.0]
    # artery.material.set_difuse(0.3)
    # artery.material.set_specular(0.2)
    # artery.material.set_shininess(100)
    blood = ObjManager()
    blood.create()
    w, h = INIT_WINDOW_SIZE
    l_y = round(tan(radians(FOVY/2))*blood.far_z, 2) * 2
    l_x = round(float(w)/h * l_y, 2) * 2
    blood.recreate_grid(l_x=l_x, l_y=l_y, cell_quantity=GRID_CELL_QUANTITY)
    blood.display()

def set_light():
    light_ambient = array([1.0, 1.0, 1.0, 1.0]) * 0.1
    light_diffuse = array([1.0, 0.0, 1.0, 1.0]) * 0.5
    light_specular = array([1.0, 1.0, 1.0, 1.0]) * 0.2
    light_position = [-40, 50, -10, 0.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, [2.0, -3.0, 2.0, 0.0])

    # ENABLE LIGHT ATTENUATION
    # glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    # glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1)
    # glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 20)
    #
    # glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1)
    # glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 1)
    # glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 5)

    glEnable(GL_LIGHT0)
    glEnable(GL_CULL_FACE)
    # glCullFace(GL_FRONT_AND_BACK)
    # glEnable(GL_LIGHT1)

def init():
    global viewport, current_w, current_h
    pygame.init()

    viewport = INIT_WINDOW_SIZE
    glutInit(sys.argv)
    # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)

    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    set_light()

    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    create_scene()

def main():
    init()
    clock = pygame.time.Clock()

    width, height = viewport
    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    zpos = max(1, zpos - 1)
                elif e.button == 5:
                    zpos += 1
                elif e.button == 1:
                    rotate = True
                elif e.button == 3:
                    move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 3:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j
        glPushMatrix()
        glTranslate(tx / 20., ty / 20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)

        display()

        glPopMatrix()

if __name__  == '__main__': main()