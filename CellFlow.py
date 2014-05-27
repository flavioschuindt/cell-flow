# This is statement is required by the build system to query build info
from OpenGL.GL.VERSION.GL_1_1 import glLightfv

if __name__ == '__build__':
    raise Exception

"""
Simple shader illumination example:
Per-fragment specular component.
"""

# Vertex shader to compute per-vertex varying half-vectors and normals
vertex_shader = """
    varying vec3 vertex_normal;
    varying vec3 half_vector;
    varying vec3 v;
    varying vec4 vTexCoord;
    void main()
    {
        vTexCoord = gl_MultiTexCoord0;
        vertex_normal = normalize(gl_NormalMatrix * gl_Normal);
        half_vector = normalize(vec3(gl_LightSource[0].halfVector));
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        v =vec3(gl_ModelViewMatrix * gl_Vertex);
    }
"""
# Fragment shader to compute the color of a fragment based on a simple
# illumination model (only specular)
fragment_shader = """
    varying vec3 vertex_normal;
    varying vec3 half_vector;
    varying vec3 v;
    uniform sampler2D myTexture;
    varying vec4 vTexCoord;
    void main()
    {
        //vec3 light_direction = normalize(vec3(gl_LightSource[0].position.xyz - v));

        vec3 vn = vertex_normal - normalize(vec3(texture2D(myTexture, vTexCoord.st).rgb));

        vec3 L = normalize(gl_LightSource[0].position.xyz - v);
        vec3 E = normalize(v);
        vec3 R = normalize(2.0 * vn * dot(L, vertex_normal) - L);

        //calculate Ambient Term:
        vec4 Iamb = gl_FrontLightProduct[0].ambient;

       //calculate Diffuse Term:

        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(vn,L), 0.0);
        Idiff = clamp(Idiff, 0.0, 1.0);

        // calculate Specular Term:
        vec4 Ispec = gl_FrontLightProduct[0].specular * pow(max(dot(R, E), 0.0), 0.3 * gl_FrontMaterial.shininess);
        Ispec = clamp(Ispec, 0.0, 1.0);

        // write Total Color:
        //FALTA COLOCAR ATENUACAO
        vec4 texel = normalize(vec4(texture2D(myTexture, vTexCoord.st).rgba));
        //gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec + texel;
        gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;
    }
"""


import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    from array import array
    from display.Obj import *
    # from display.BumpTeste import *
    from pyglsl import *
    from OpenGL.GL import shaders

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
    light_position = array([1.0, 3.0, -3.5, 0.0]) * 10.0
    # [3.0, -1.0, 3.0, 0.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    # glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.0)
    # glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0)
    # glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.1)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, [-1.0, 1.0, 2.0, 0.0])

    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)

    create_scene()
    global program
    program = compile_program (vertex_shader, fragment_shader)
    # glUseProgram(program)

def display():
    glUseProgram(0)
    glClearColor(1, 0.5, 0, 1)
    glClearDepth(1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(program)
    print " display"
    glLoadIdentity()  # clear the matrix
    # view transformation
    gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

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
    global fundo
    if key == 'w':
        fundo.material.set_shininess(fundo.material.shininess + 0.5)
    elif key == 'q':
        fundo.material.set_shininess(fundo.material.shininess - 0.5)
    elif key == 's':
        fundo.material.set_specular(fundo.material.specular + 0.02)
    elif key == 'a':
        fundo.material.set_specular(fundo.material.specular - 0.02)
    elif key == 'x':
        fundo.material.set_difuse(fundo.material.difuse + 0.02)
    elif key == 'z':
        fundo.material.set_difuse(fundo.material.difuse - 0.02)

    glutPostRedisplay()
    if key == chr(27):
        import sys
        sys.exit(0)

def create_scene():
    global display_list, fundo
    display_list = []
    fundo = Obj()
    display_list.append(fundo)

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
