import pygame
from vec import vec


class Body(pygame.Rect):
	def __init__(self, rect):
		super().__init__(rect.left, rect.top, rect.width, rect.height)
		self.real = vec(self.x, self.y)
		self.standing = False
		self.ontops = set()
		self.underneaths = set()
		# Physics properties
		self.velocity = vec()
		self.dumping = vec(0.01)
		self.friction = vec(0.03, 0)
		self.restitution = 0.2
		self.mass = 1.0

	def __hash__(self):
		return id(self)

	def move(self, offset):
		# Apply movement
		self.real += offset
		# Update integer coordinates
		self.x = int(self.real.x)
		self.y = int(self.real.y)
		# Recursively move bodies stacked on top
		if abs(offset.x) > 0:
			for body in self.ontops:
				body.move(vec(offset.x, 0))
			
	def set(self, position):
		# Overwrite position
		self.real = position
		# Update integer coordinates
		self.x = int(self.real.x)
		self.y = int(self.real.y)

	def stop(self, x=True, y=True):
		"""Set body into a stable state where it is not moving and evenly
		aligned to the pixel grid"""
		if x:
			self.velocity.x = 0
			self.real.x = self.x
		if y:
			self.velocity.y = 0
			self.real.y = self.y

	def reinitialize(self, x=False, y=False):
		"""Update float value coordinates from grid position, should
		be used after setting a coordinate with e.g. body.left"""
		if x:
			self.real.x = float(self.x)
		if y:
			self.real.y = float(self.y)

	def stands_on(self, body):
		threshold = 2
		feet = pygame.Rect(self.left, self.bottom - threshold, self.width, 2 * threshold)
		return feet.colliderect(body)

	def detach(self):
		"""Detach body from physics simulation, by updating touching bodies"""
		for other in self.ontops:
			other.underneaths.discard(self)
			if len(other.underneaths) < 1:
				other.standing = False
		for other in self.underneaths:
			other.ontops.discard(self)

	def bounce_from(self, other, magnitude=700.0):
		"""Bounce away from another body"""
		# Calculate direction
		offset = vec(0, -32)
		normal = (self.real - other.real + offset).normalize()
		# Apply bounce
		restitution = min(self.restitution, other.restitution)
		overall_mass = self.mass + other.mass
		self.velocity = normal * magnitude / overall_mass
		# Remove bodies from each other
		other.ontops.discard(self)
		other.underneaths.discard(self)
		self.ontops.discard(other)
		self.underneaths.discard(other)

	def collide_upper(self, other):
		"""Check if overlapping with a rectangle, but ignore the bottom pixel.
		Useful to check if touching another body from the side but not standing
		on top of it."""
		upper = pygame.Rect(self.left - 1, self.top, self.w + 2, self.h - 1)
		return upper.colliderect(other)
