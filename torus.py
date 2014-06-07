from math import pi, cos, sin, radians, tan
import itertools

from vector import PVector


class Torus:
	newid = itertools.count().next

	def __init__(self, color, location, inner_radius, outter_radius, 
				 sides, rings, mass, max_speed, max_force, obj):
		self.inner_radius = inner_radius
		self.outter_radius = outter_radius
		self.sides = sides
		self.rings = rings
		self.x_rotated = 0
		self.y_rotated = 0
		self.z_rotated = 0
		self.color = color
		self.max_speed = max_speed
		self.max_force = max_force
		self.id = Torus.newid()
		
		self.points = []
		self.matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

		# Object forces and mass
		self.location = PVector(*location)
		self.velocity = PVector()
		self.acceleration = PVector()
		self.mass = mass
		# Translate object to initial position
		self.translate(self.location.x, self.location.y, self.location.z)

		# Config material properties: texture and material
		self.obj = obj

	def apply_force(self, force):
		f = PVector.div(force, self.mass)
		self.acceleration.add(f)

	def update(self, aspect, fovy):

		self.velocity.add(self.acceleration)
		self.location.add(self.velocity)
		self._check_edges(aspect, fovy)

		self.acceleration.mult(0)

	def _check_edges(self, aspect, fovy):

		limit_y = round(tan(radians(fovy/2))*-1*self.location.z, 2)
		limit_x = round(aspect * limit_y, 2)

		if self.location.x > limit_x:
			self.location.x = limit_x
			self.velocity.x *= -1
		elif self.location.x < -1*limit_x:
			self.location.x = -1*limit_x
			self.velocity.x *= -1

		if self.location.y > limit_y:
			self.velocity.y *= -1
			self.location.y = limit_y
		elif self.location.y < -1*limit_y:
			self.velocity.y *= -1
			self.location.y = -1*limit_y

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
		return self.points

	def flock(self, scene, desired_separation):
		sep = self.separate(scene, desired_separation)   # Separation
		self.apply_force(sep)

  	# Separation
  	# Method checks for nearby torus and steers away
  	def separate(self, scene, desired_separation):
    
		steer = PVector(0.0, 0.0, 0.0)
		count = 0
		# For every torus in the system, check if it's too close
		for torus in scene:
			d = PVector.distance(self.location, torus.location)
			# If the distance is greater than 0 and less than an arbitrary amount (0 when you are yourself)
			if d > 0 and d < desired_separation:
				# Calculate vector pointing away from neighbor
				diff = PVector.sub(self.location, torus.location)
				diff = PVector.normalize(diff)
				diff = PVector.div(diff, d) # Weight by distance
				steer.add(diff)
				count += 1 #Keep track of how many
		
		# Average -- divide by how many
		if count > 0:
			steer = PVector.div(steer, float(count))

		# As long as the vector is greater than 0
		if PVector.magnitude(steer) > 0:
			# Implement Reynolds: Steering = Desired - Velocity
			steer = PVector.normalize(steer)
			steer.mult(self.max_speed)
			steer = PVector.sub(steer, self.velocity)
			steer = PVector.limit(steer, self.max_force)

		return steer




