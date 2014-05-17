from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random
from vector import PVector

from torus import Torus
from const import FRAME_PERIOD, INIT_WINDOW_SIZE, INIT_WINDOW_POSITION, \
				  BACKGROUND_COLOR, TORUS_SIDES, TORUS_RINGS, TORUS_COLOR, \
				  TORUS_INNER_RADIUS, TORUS_OUTTER_RADIUS, TORUS_MASS_RANGE, \
				  TORUS_QUANTITY, FOVY, Z_NEAR, Z_FAR, FLUID_FORCE, GRAVITY_FORCE_FACTOR

scene = []
current_w = 0
current_h = 0

def display():
	global scene
	# clear the drawing buffer.
	glClear(GL_COLOR_BUFFER_BIT)
	for torus in scene:

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glColor3f(*torus.color)
		glPushMatrix()
		glMultMatrixf(torus.matrix)

		points = torus.calc_points()

		glBegin(GL_QUAD_STRIP)
		for point in torus.points:
			glVertex3d(*point)
		glEnd()

		glPopMatrix()
		glFlush()

	glutSwapBuffers()

def reshape(w, h):
	global current_w, current_h
	if w == 0 or h == 0:
		return

	current_w = w
	current_h = h

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(FOVY, float(w)/h, Z_NEAR, Z_FAR)

	glViewport(0, 0, w, h)
	glMatrixMode(GL_MODELVIEW)
	glutPostRedisplay()

def timer(value):
	global scene
	if scene[1].is_colliding_with(scene[0]):
			print 'Pode colidir!'

	fluid = PVector(*FLUID_FORCE)
	for index, torus in enumerate(scene):
		gravity = PVector(0, GRAVITY_FORCE_FACTOR*torus.mass)
		if index == 1:
			torus.apply_force(fluid)
			torus.apply_force(gravity)
		torus.update(float(current_w)/current_h, FOVY)

	display()
	glutTimerFunc(FRAME_PERIOD, timer, 0)

def main():
	global scene
	for x in range(TORUS_QUANTITY):
		mass = random.uniform(*TORUS_MASS_RANGE)
		location_x = 0
		location_y = 0 if x == 0 else 3
		location_z = 4
		t = Torus(
				 sides=TORUS_SIDES, 
				 rings=TORUS_RINGS, 
				 color=TORUS_COLOR, 
				 location=(location_x, location_y, -1*location_z), 
				 inner_radius=TORUS_INNER_RADIUS, 
				 outter_radius=TORUS_OUTTER_RADIUS, 
				 mass=mass
				 )
		scene.append(t)

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