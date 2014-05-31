# This is statement is required by the build system to query build info

if __name__ == '__build__':
    raise Exception

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    from array import array
    from display.Obj import *
    # from display.BumpTeste import *
    from OpenGL.GL import shaders
    from shaders.Shaders import *
    # from shaders.ShadersVELHO import *
    # from Camera import *
except:
    print '''
ERROR: PyOpenGL not installed properly.
        '''
current_w = 720
current_h = 480

def init():
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glEnable(GL_TEXTURE_2D)

    # glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    light_ambient = [1.0, 1.0, 1.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = array([-2.0, -2.0, 0.5, 0.0])

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # ENABLE LIGHT ATTENUATION
    # glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    # glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1)
    # glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 5)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, [2.0, -3.0, 2.0, 0.0])

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


    # glUseProgram(program)

    create_scene()

def display():
    glUseProgram(0)
    glClearColor(1, 0.5, 0, 1)
    glClearDepth(1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    print " display"
    glLoadIdentity()  # clear the matrix
    # view transformation
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    total = len(display_list)
    for i in range(0, total, 1):
        display_list[i].display()

    glutSwapBuffers()


def reshape(w, h):
    global current_w, current_h
    current_w = w
    current_h = h
    glViewport(0, 0, current_w, current_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(20, w*1.0/h, 0, 100)
    glMatrixMode(GL_MODELVIEW)
    print "reshape"

def keyboard(key, x, y):
    global sphere

    if key == 'w':
        sphere.material.set_shininess(sphere.material.shininess + 0.5)
    elif key == 'q':
        sphere.material.set_shininess(sphere.material.shininess - 0.5)
    elif key == 's':
        sphere.material.set_specular(sphere.material.specular + 0.02)
    elif key == 'a':
        sphere.material.set_specular(sphere.material.specular - 0.02)
    elif key == 'x':
        sphere.material.set_difuse(sphere.material.difuse + 0.02)
    elif key == 'z':
        sphere.material.set_difuse(sphere.material.difuse - 0.02)
    elif(key == "r"):
        sphere.rotation += 1

    glutPostRedisplay()
    if key == chr(27):
        import sys
        sys.exit(0)

def create_scene():
    global display_list, sphere, program
    display_list = []
    sphere = Obj()
    display_list.append(sphere)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA )
glutInitWindowSize(current_w, current_h)
glutInitWindowPosition(100, 100)
glutCreateWindow('sphere')
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
init()
glutMainLoop()

__author__ = 'bruno'
