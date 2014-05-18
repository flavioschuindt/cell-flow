from math import sqrt

class PVector:
	def __init__(self, x=0, y=0, z=0):
		self.x = x
	 	self.y = y
	 	self.z = z

	def add(self, u):
	 	self.x += u.x
	 	self.y += u.y
	 	self.z += u.z

	def mult(self, s): # Multiply by scalar
	 	self.x *= s
	 	self.y *= s
	 	self.z *= s

	@staticmethod
	def div(u, v): # Division by scalar
	 	r = PVector()
	 	r.x = u.x / v
	 	r.y = u.y / v
	 	r.z = u.z / v
	 	return r

	@staticmethod
	def sub(u, v):
	 	r = PVector()
	 	r.x = u.x - v.x
	 	r.y = u.y - v.y
	 	r.z = u.z - v.z
	 	return r

	@staticmethod
	def square(u):
		r = PVector()
		r.x = u.x * u.x
		r.y = u.y * u.y
		r.z = u.z * u.z
		return r

	@staticmethod
	def magnitude(u):
		return sqrt( (u.x ** 2) + (u.y ** 2) + (u.z ** 2) )

	@staticmethod
	def normalize(u):
		return PVector.div(u, PVector.magnitude(u))

	@staticmethod
	def dot(u, v):
		return u.x*v.x + u.y*v.y + u.z*v.z

	@staticmethod
	def distance(u, v):
		diff = PVector.sub(u, v)
		return PVector.magnitude(diff)

	@staticmethod
	def limit(u, mag):
		if PVector.magnitude(u) > mag:
			a_b = a_c = 0
			if u.y != 0:
				a_b = float(u.x)/u.y
				y2 = u.y ** 2
			else:
				y2 = 0.0
			
			if u.z != 0:
				a_c = float(u.x)/u.z
				z2 = u.z ** 2
			else:
				z2 = 0.0
			
			a = sqrt(float((mag ** 2))/(1 + y2 + z2))
			b = a / a_b if a_b != 0 else 0.0
			c = a / a_c if a_c != 0 else 0.0

			limited_vector = PVector(a, b, c)

			return limited_vector
		
		return u

	def __repr__(self):
		return 'Point(x=%s, y=%s, z=%s)' % (self.x, self.y, self.z)