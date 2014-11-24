import math
import pygame
from vec import vec


class Body(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		delta = 1 / 60
		self.movement(delta)
		self.collision()
		self.inside_window()
		self.velocity(delta)

	def movement(self, delta):
		"""Move all bodies according to their velocity"""
		for body in self.engine.entities.bodies.values():
			# Move body by velocity given in meters per second
			pixel_per_meter = 32
			body.move(body.velocity * delta * pixel_per_meter)
		# Since bodies have moved, relations among them may have become invalid
		for body in self.engine.entities.bodies.values():
			body.on_ground = False
			# See if stacked objects are still on top, otherwise remove from set
			for other in body.on_tops.copy():
				pixel_below = pygame.Rect(other.left, other.top, other.width, other.height + 1)
				if not body.colliderect(pixel_below):
					body.on_tops.discard(other)

	def collision(self):
		"""Resolve collisions between bodies"""
		pairs = self.get_intersecting()
		for one, two in pairs:
			overlap = one.clip(two)
			overlap.normalize()
			# Resolve along axis with smaller intersection
			if overlap.w < overlap.h:
				# Horizontal overlap
				if one.x < two.x:
					self.move_apart(one, two, vec(-overlap.w, 0))
				else:
					self.move_apart(one, two, vec(+overlap.w, 0))
			else:
				# Vertical overlap
				if one.y < two.y:
					self.move_apart(one, two, vec(0, -overlap.h))
					one.on_ground = True
					if one.mass > 0:
						two.on_tops.add(one)
				else:
					self.move_apart(one, two, vec(0, +overlap.h))
					two.on_ground = True
					if two.mass > 0:
						one.on_tops.add(two)

	def velocity(self, delta):
		"""Update velocity for the next frame"""
		for body in self.engine.entities.bodies.values():
			# Skip static bodies
			if body.mass == 0:
				continue
			# Bounce from window border
			if body.left < 0 or body.right > self.engine.width:
				body.velocity.x *= -body.restitution
			if body.top < 0 or body.bottom > self.engine.height:
				body.velocity.y *= -body.restitution
			# Apply gravity while in the air, on the
			# ground prevent from trying to move further
			gravity = 15.0
			if not body.on_ground:
				body.velocity.y += gravity * delta
			else:
				body.velocity.y = min(body.velocity.y, 0)
			# Dump velocity to simulate air drag
			body.velocity.x *= max(1 - body.dumping.x, 0)
			body.velocity.y *= max(1 - body.dumping.y, 0)
			# Simulate friction when on the ground
			if body.on_ground:
				body.velocity.x *= max(1 - body.friction.x, 0)
				body.velocity.y *= max(1 - body.friction.y, 0)

	def inside_window(self):
		"""Keep bodies inside window area"""
		for body in self.engine.entities.bodies.values():
			if body.top < 0:
				body.top = 0
				body.reinitialize(x=False, y=True)
			elif body.bottom > self.engine.height:
				body.bottom = self.engine.height
				body.reinitialize(x=False, y=True)
				body.on_ground = True
			if body.left < 0:
				body.left = 0
				body.reinitialize(x=True, y=False)
			elif body.right > self.engine.width:
				body.right = self.engine.width
				body.reinitialize(x=True, y=False)

	def get_intersecting(self):
		"""Get all pairs of intersection bodies"""
		pairs = []
		bodies = list(self.engine.entities.bodies.values())
		for i, one in enumerate(bodies):
			for j, two in enumerate(bodies[i + 1:]):
				if one.mass == 0 and two.mass == 0:
					continue
				if one.colliderect(two):
					pairs.append((one, two))
		return pairs

	def move_apart(self, one, two, vector):
		# Move modies away
		if one.mass == 0 and two.mass == 0:
			pass
		elif one.mass > 0 and two.mass == 0:
			one.move(vector)
		elif one.mass == 0 and two.mass > 0:
			two.move(-vector)
		elif one.mass > 0 and two.mass > 0:
			one.move(vector / 2)
			two.move(-vector / 2)
