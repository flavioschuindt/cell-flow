import random
from math import radians, tan

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
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
		glColor3f(*torus.color)
		glPushMatrix()
		glLoadIdentity()
		glMultMatrixf(torus.matrix)

		points = torus.calc_points() if len(torus.points) == 0 else torus.points

		glBegin(GL_QUAD_STRIP)
		for point in points:
			glVertex3d(*point)
		glEnd()

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

def main():
	global scene, far_z
	w, h = INIT_WINDOW_SIZE
	aspect = float(w) / h
	z_values = []
	for x in range(TORUS_QUANTITY):
		mass = random.uniform(*TORUS_MASS_RANGE)
		location_z = 6#random.uniform(Z_NEAR, Z_FAR)
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
				 max_force=TORUS_FLOCKING_MAX_FORCE
				 )
		scene.append(t)

	far_z = max(z_values)

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(*INIT_WINDOW_SIZE)
	glutInitWindowPosition(*INIT_WINDOW_POSITION)
	glutCreateWindow("Torus")
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glClearColor(*BACKGROUND_COLOR)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(FRAME_PERIOD, timer, 0)
	glutMainLoop()
	return 0

if __name__  == '__main__': main()