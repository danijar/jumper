import math


class vec(object):
	"""Two dimensional vector providing arithmetic operators"""
	def __init__(self, x=None, y=None):
		if x is None:
			x = 0.0
		if y is None:
			y = x
		self.x = float(x)
		self.y = float(y)
	def as_list(self, integer=False):
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
		if isinstance(other, (int, float)):
			try:
				return vec(self.x / other, self.y / other)
			except ZeroDivisionError:
				return self
		else:
			raise TypeError()
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
