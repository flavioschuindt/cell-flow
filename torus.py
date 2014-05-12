from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import pi, cos, sin
import random
from vector import PVector
 
scene = []
factor = 1

class Torus:

	def __init__(self, color, location, inner_radius=1, outter_radius=0.2, sides=50, rings=50, mass=1):

		self.inner_radius = inner_radius
		self.outter_radius = outter_radius
		self.sides = sides
		self.rings = rings
		self.x_rotated = 0
		self.y_rotated = 0
		self.z_rotated = 0
		self.color = color
		
		self.points = []
		self.matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

		# Object forces and mass
		self.location = PVector(*location)
		self.velocity = PVector()
		self.acceleration = PVector()
		self.mass = mass
		# Translate object to initial position
		self.translate(self.location.x, self.location.y, self.location.z)

	def apply_force(self, force):
		f = PVector.div(force, self.mass)
		self.acceleration.add(f)

	def update(self):
		self.velocity.add(self.acceleration)
		self.location.add(self.velocity)
		self.translate(self.location.x, self.location.y, self.location.z)

		self.acceleration.mult(0)

	def check_edges(self):

		if self.location.x > 4:
			self.location.x = 4
			self.velocity.x *= -1
		elif self.location.x < 0:
			self.velocity.x *= -1
			self.location.x = 0

		if self.location.y > 4:
			self.velocity.y *= -1
			self.location.y = 4

	def translate(self, x=0, y=0, z=0):
		self.matrix[12] = x
		self.matrix[13] = y
		self.matrix[14] = z

	def rotate(self, x=0, y=0, z=0):
		self.x_rotated += x
		self.y_rotated += y
		self.z_rotated += z

	def calc_points(self):
		self.points = []
		two_pi = pi * 2
		a = self.outter_radius
		c = self.inner_radius + self.outter_radius
		for i in range(self.sides):
			for j in range(self.rings + 1):
				k = 1
				while k >= 0:
					s = (i + k) % self.sides + 0.5
					t = j % self.rings

					x = (c + a * cos(s * two_pi / self.sides)) * cos(t * two_pi / self.rings)
					y = (c + a * cos(s * two_pi / self.sides)) * sin(t * two_pi / self.rings) 
					z = a * sin(s * two_pi / self.sides)
					k -= 1
					self.points.append((x, y, z))

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
	global factor

	wind = PVector(-0.1, 0)
	for torus in scene:
		gravity = PVector(0, -0.01*torus.mass)
		torus.apply_force(wind)
		torus.apply_force(gravity)
		torus.update()
		#torus.check_edges()

	display()

def main():
	global scene
	for x in range(20):
		mass = random.uniform(0, 200)
		location_x = random.uniform(0, 3)
		location_y = random.uniform(0, 3)
		location_z = random.uniform(5, 6)
		t = Torus(
				 sides=100, 
				 rings=50, 
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