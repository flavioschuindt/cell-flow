

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