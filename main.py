from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random
from vector import PVector

from torus import Torus

scene = []

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

def reshape(x, y):
	if y == 0 or x == 0:
		return
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(40.0, x/y, 0.5, 20.0)

	glViewport(0, 0, x, y)
	glMatrixMode(GL_MODELVIEW)
	glutPostRedisplay()

def idle():
	global scene
	if scene[1].is_colliding_with(scene[0]):
			print 'Pode colidir!'

	fluid = PVector(-0.1, 0)
	for index, torus in enumerate(scene):
		gravity = PVector(0, -0.01*torus.mass)
		if index == 1:
			torus.apply_force(fluid)
			torus.apply_force(gravity)
		torus.update()
		torus.check_edges()

	display()

def main():
	global scene
	for x in range(2):
		mass = random.uniform(0, 200)
		location_x = 0#random.uniform(-1, 1)
		location_y = 0 if x == 0 else 3#random.uniform(-1, 1)
		location_z = 4#random.uniform(5, 6)
		t = Torus(
				 sides=40, 
				 rings=300, 
				 color=(1,0,0), 
				 location=(location_x, location_y, -1*location_z), 
				 inner_radius=0, 
				 outter_radius=0.03, 
				 mass=mass
				 )
		scene.append(t)

	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(800, 800)
	glutInitWindowPosition(450, 200)
	glutCreateWindow("Torus")
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)
	glutMainLoop()
	return 0

if __name__  == '__main__': main()