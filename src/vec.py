import math


class vec(object):
	"""Two dimensional vector providing arithmetic operators"""
	def __init__(self, *args):
		count = len(args)
		one = args[0] if count > 0 else None
		two = args[1] if count > 1 else None
		if count == 0:
			self.x = 0
			self.y = 0
		elif count == 1 and isinstance(one, (int, float)):
			self.x = one
			self.y = one
		elif count >= 1 and isinstance(one, object) and hasattr(one, 'x') and hasattr(one, 'y'):
			self.x = one.x
			self.y = one.y
		elif count >= 1 and isinstance(one, (list, tuple)) and len(one) == 2:
			self.x = one[0]
			self.y = one[1]
		elif count == 2 and isinstance(one, (int, float)) and isinstance(two, (int, float)):
			self.x = one
			self.y = two
		else:
			raise TypeError()
		self.x = float(self.x)
		self.y = float(self.y)
	def list(self, integer=True):
		# Useful for interfaces that expect coordinates as lists
		if integer:
			# Useful for rendering inside a pixel grid
			return [int(self.x), int(self.y)]
		else:
			return [self.x, self.y]
	def length(self):
		dot = (self.x * self.x) + (self.y * self.y)
		return math.sqrt(dot)
	def normalize(self):
		return self / self.length()
	def dot(self, other):
		return (self.x * other.x) + (self.y * other.y)
	def __pos__(self):
		return vec(self)
	def __neg__(self):
		return vec(-self.x, -self.y)
	def __pos__(self):
		return vec(self.x, self.y)
	def __add__(self, other):
		if isinstance(other, vec):
			return vec(self.x + other.x, self.y + other.y)
		elif isinstance(other, (int, float)):
			return vec(self.x + other, self.y + other)
		else:
			raise TypeError()
	def __sub__(self, other):
		return self.__add__(-other)
	def __mul__(self, other):
		if isinstance(other, vec):
			# Multiplication of two vectors is element wise
			return vec(self.x * other.x, self.y * other.y)
		elif isinstance(other, (int, float)):
			return vec(self.x * other, self.y * other)
		else:
			raise TypeError()
	def __truediv__(self, other):
		try:
			if isinstance(other, vec):
				return vec(self.x / other.x, self.y / other.y)
			elif isinstance(other, (int, float)):
				return vec(self.x / other, self.y / other)
			else:
				raise TypeError()
		except ZeroDivisionError:
			return self
	def __iadd__(self, other):
		if isinstance(other, vec):
			self.x += other.x
			self.y += other.y
		elif isinstance(other, (int, float)):
			self.x += other
			self.y += other
		else:
			raise TypeError()
		return self
	def __isub__(self, other):
		return self.__iadd__(-other)
	def __imul__(self, other):
		if isinstance(other, vec):
			self.x *= other.x
			self.y *= other.y
		elif isinstance(other, (int, float)):
			self.x *= other
			self.y *= other
		else:
			raise TypeError()
		return self
	def __itruediv__(self, other):
		if isinstance(other, (int, float)):
			self.x /= other
			self.y /= other
		else:
			raise TypeError()
		return self
	def __nonzero__(self):
		return self.x or self.y
	def __abs__(self):
		return vec(abs(self.x), abs(self.y))
	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ')'
