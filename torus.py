from math import pi, cos, sin, sqrt
from vector import PVector


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

		if self.location.x > 1:
			self.location.x = 1
			self.velocity.x *= -1
		elif self.location.x < -1:
			self.velocity.x *= -1
			self.location.x = -1

		if self.location.y > 1:
			self.velocity.y *= -1
			self.location.y = 1
		elif self.location.y < -1:
			self.velocity.y *= -1
			self.location.y = -1

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

	def is_colliding_with(self, t):
		'''delta = PVector.sub(self.location, t.location)
		delta_squared = PVector.square(delta)
		sum_radius_squared = ((self.inner_radius + self.outter_radius) + (t.inner_radius + t.outter_radius)) ** 2

		return ((delta_squared.x + delta_squared.y) <= sum_radius_squared)'''

		'''
			Test #1: If the length of the velocity vector is less than distance between the centers of the spheres minus 
			their radius, there's no way they can hit.
		'''
		distance = PVector.magnitude(PVector.sub(self.location, t.location))
		sum_radius = ((self.inner_radius + self.outter_radius) + (t.inner_radius + t.outter_radius))
		velocity_mag = PVector.magnitude(self.velocity)
		if velocity_mag < (distance - sum_radius):
			return False

		'''
			Test #2: Make sure that A is moving towards B.
		'''
		n = PVector.normalize(self.velocity)
		c = PVector.sub(t.location, self.location)
		d = PVector.dot(n, c)
		if d <= 0:
			return False

		f = (distance * distance) - (d * d) # Pitagoras' Theorem
		sum_radius_squared = sum_radius * sum_radius

		'''
			Test #3: If the closest that A will get to B is more than the sum of their radius, 
			there's no way they are going collide
		'''
		if f >= sum_radius_squared:
			return False

		s = sum_radius_squared - f
		if s < 0:
			return False
		
		'''
			Test #4: The limit that the moving sphere can move without touch the static sphere is: limit = d - sqrt(t).
			So, we should make sure that the distance the moving sphere A has to move to touch static sphere B is not greater
			than the velocity magnitude.
		'''

		limit = d - sqrt(s)
		if velocity_mag < limit:
			return False

		return True




