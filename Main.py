# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from const import FRAME_PERIOD, INIT_WINDOW_SIZE, INIT_WINDOW_POSITION, \
    BACKGROUND_COLOR, TORUS_SIDES, TORUS_RINGS, TORUS_COLOR, \
    TORUS_INNER_RADIUS, TORUS_OUTTER_RADIUS, TORUS_MASS_RANGE, \
    TORUS_QUANTITY, FOVY, Z_NEAR, Z_FAR, FLUID_FORCE, GRAVITY_FORCE_FACTOR, \
    TORUS_DESIRED_SEPARATION, TORUS_FLOCKING_MAX_SPEED, TORUS_FLOCKING_MAX_FORCE, \
    GRID_CELL_QUANTITY
from math import tan, radians
from grid import Grid
from vector import PVector
from torus import Torus
import random
from display.Obj import *

# IMPORT OBJECT LOADER
from objloader import *

viewport = INIT_WINDOW_SIZE
grid = None
scene = []
current_w = 0
current_h = 0
far_z = 0
artery = None


def keyboard(key, x, y):
    global sphere
    for torus in scene:
        if key == 'w':
            torus.obj.material.set_shininess(torus.obj.material.shininess + 0.5)
        elif key == 'q':
            torus.obj.material.set_shininess(torus.obj.material.shininess - 0.5)
        elif key == 's':
            torus.obj.material.set_specular(torus.obj.material.specular + 0.02)
        elif key == 'a':
            torus.obj.material.set_specular(torus.obj.material.specular - 0.02)
        elif key == 'x':
            torus.obj.material.set_difuse(torus.obj.material.difuse + 0.02)
        elif key == 'z':
            torus.obj.material.set_difuse(torus.obj.material.difuse - 0.02)
        elif(key == "r"):
            torus.obj.rotation += 1

    glutPostRedisplay()
    if key == chr(27):
        import sys
        sys.exit(0)

def timer():
    global scene, grid
    fluid = PVector(*FLUID_FORCE)
    for index, torus in enumerate(scene):
        gravity = PVector(0, GRAVITY_FORCE_FACTOR*torus.mass)
        grid.remove(torus)
        torus.apply_force(fluid)
        torus.apply_force(gravity)
        torus.update(float(current_w)/current_h, FOVY)
        torus.flock(grid.get_neighbors(torus), TORUS_DESIRED_SEPARATION)
        torus.translate(torus.location.x, torus.location.y, torus.location.z)
        grid.insert(torus)

    display()


def display():
    global scene, obj
    # clear the drawing buffer.
    glClear(GL_COLOR_BUFFER_BIT)
    for torus in scene:
        glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        glPushMatrix()
        glMultMatrixf(torus.matrix)

        points = torus.calc_points() if len(torus.points) == 0 else torus.points

        torus.obj.display()
        glPopMatrix()
    glCallList(artery.gl_list)
    pygame.display.flip()
    # glutSwapBuffers()


def reshape(w, h):
    global current_w, current_h, grid, far_z
    if w == 0 or h == 0:
        return

    current_w = w
    current_h = h

    ar = float(w)/h
    l_y = round(tan(radians(FOVY/2))*-1*far_z, 2)
    l_x = round(ar * l_y, 2)

    grid = Grid(
                width=l_x * 2,
                height=l_y * 2,
                cell_quantity=GRID_CELL_QUANTITY
                )

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, ar, Z_NEAR, Z_FAR)

    glViewport(0, 0, w, h)
    glMatrixMode(GL_MODELVIEW)
    # glutPostRedisplay()

def init():
    global viewport
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    pygame.init()
    viewport = (800, 600)
    hx = viewport[0] / 2
    hy = viewport[1] / 2
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glClearColor(*BACKGROUND_COLOR)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(FRAME_PERIOD, timer, 0)
    glutKeyboardFunc(keyboard)

    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glEnable(GL_TEXTURE_2D)

    # glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    light_ambient = [1.0, 1.0, 1.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [0.0, 0.0, -3, 0.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # ENABLE LIGHT ATTENUATION
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 5)

    glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 1)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 5)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, [2.0, -3.0, 2.0, 0.0])

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_COLOR_MATERIAL)



def main():
    global scene, far_z, artery
    w, h = INIT_WINDOW_SIZE
    z_values = []
    init()
    # LOAD OBJECT AFTER PYGAME INIT
    # obj = OBJ(sys.argv[1], swapyz=True)
    artery = OBJ("veia.obj")

    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width / float(height), 1, 100.0)
    # glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False



    init()
    for x in range(TORUS_QUANTITY):
        mass = random.uniform(*TORUS_MASS_RANGE)
        location_z = 2#random.uniform(Z_NEAR, Z_FAR)
        z_values.append(-1*location_z)
        location_x = 0
        location_y = 0
        t = Torus(
                 sides=TORUS_SIDES,
                 rings=TORUS_RINGS,
                 color=TORUS_COLOR,
                 location=(location_x, location_y, -1*location_z),
                 inner_radius=TORUS_INNER_RADIUS,
                 outter_radius=TORUS_OUTTER_RADIUS,
                 mass=mass,
                 max_speed=TORUS_FLOCKING_MAX_SPEED,
                 max_force=TORUS_FLOCKING_MAX_FORCE,
                 obj=Obj(size=TORUS_INNER_RADIUS + 2*TORUS_OUTTER_RADIUS, model = "hemacia.obj")
                 )
        scene.append(t)

    far_z = max(z_values)
    reshape(*viewport)
    #glutMainLoop()
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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # RENDER OBJECT
        #
        # glRotate(ry, 1, 0, 0)
        # glRotate(rx, 0, 1, 0)
        glPushMatrix()
        glTranslate(tx / 20., ty / 20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        timer()
        glPopMatrix()
    return 0

if __name__  == '__main__': main()