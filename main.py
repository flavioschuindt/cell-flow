from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from display.Obj import *
import random
from math import tan, radians

from vector import PVector
from torus import Torus
from const import FRAME_PERIOD, INIT_WINDOW_SIZE, INIT_WINDOW_POSITION, \
				  BACKGROUND_COLOR, TORUS_SIDES, TORUS_RINGS, TORUS_COLOR, \
				  TORUS_INNER_RADIUS, TORUS_OUTTER_RADIUS, TORUS_MASS_RANGE, \
				  TORUS_QUANTITY, FOVY, Z_NEAR, Z_FAR, FLUID_FORCE, GRAVITY_FORCE_FACTOR, \
				  TORUS_DESIRED_SEPARATION, TORUS_FLOCKING_MAX_SPEED, TORUS_FLOCKING_MAX_FORCE, \
				  GRID_CELL_QUANTITY

from grid import Grid


grid = None
scene = []
current_w = 0
current_h = 0
far_z = 0

def display():
    global scene
    # clear the drawing buffer.
    glClear(GL_COLOR_BUFFER_BIT)
    for torus in scene:
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #glColor3f(*torus.color)
        glPushMatrix()
        glMultMatrixf(torus.matrix)

        points = torus.calc_points() if len(torus.points) == 0 else torus.points

        '''glBegin(GL_QUAD_STRIP)
        for point in points:
            glVertex3d(*point)
        glEnd()'''

        torus.obj.display()
        glPopMatrix()
        glFlush()
    glutSwapBuffers()

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
	glutPostRedisplay()

def timer(value):
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
	glutTimerFunc(FRAME_PERIOD, timer, 0)

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

def init():

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(*INIT_WINDOW_SIZE)
	glutInitWindowPosition(*INIT_WINDOW_POSITION)
	glutCreateWindow("Torus")
	# glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
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

def main():
	global scene, far_z
	w, h = INIT_WINDOW_SIZE
	aspect = float(w) / h
	z_values = []
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
				 obj=Obj(size=TORUS_INNER_RADIUS + 2*TORUS_OUTTER_RADIUS)
				 )
		scene.append(t)

	far_z = max(z_values)
	
	glutMainLoop()
	return 0

if __name__  == '__main__': main()