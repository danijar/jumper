import math
import pygame
from vec import vec


class Body(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		delta = 1 / 60

		self.on_ground()
		self.movement(delta)
		self.collision()
		self.inside_window()
		self.velocity(delta)
		#self.on_ground()

		# Debugging
		on_ground = 0
		for body in self.engine.entities.bodies.values():
			if body.on_ground:
				on_ground += 1
		print('\rOverall', len(self.engine.entities.bodies), 'and', on_ground, 'on ground')

	def movement(self, delta):
		"""Move all bodies according to their velocity"""
		for body in self.engine.entities.bodies.values():
			# Move body by velocity given in meters per second
			pixels_per_meter = 32
			body.move(body.velocity * delta * pixels_per_meter)

	def on_ground(self):
		# Since bodies have moved, relations among them may have become invalid
		for body in self.engine.entities.bodies.values():
			# See if stacked objects are still on top
			for other in body.ontops.copy():
				if not other.stands_on(body):
					body.ontops.discard(other)
			# See if still on top of underneath objects
			for other in body.underneaths.copy():
				if not body.stands_on(other):
					body.underneaths.discard(other)
			# Update on ground property
			has_underneaths = len(body.underneaths) > 0
			window_bottom = body.bottom >= self.engine.height
			body.on_ground = has_underneaths or window_bottom

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
					# Stack dynamic bodies but stop movement at static ones
					if one.mass > 0:
						one.underneaths.add(two)
						two.ontops.add(one)
					else:
						two.velocity.y = max(two.velocity.y, 0)
				else:
					self.move_apart(one, two, vec(0, +overlap.h))
					# Stack dynamic bodies but stop movement at static ones
					if two.mass > 0:
						two.underneaths.add(one)
						one.ontops.add(two)
					else:
						one.velocity.y = max(one.velocity.y, 0)

	def velocity(self, delta):
		"""Update velocity for the next frame"""
		for body in self.engine.entities.bodies.values():
			# Skip static bodies
			if body.mass == 0:
				continue
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
			# Skip static bodies
			if body.mass == 0:
				continue
			# Bounce from window border
			if body.top < 0:
				body.velocity.y *= -body.restitution
				body.top = 0
				body.reinitialize(y=True)
			elif body.bottom > self.engine.height:
				body.velocity.y *= -body.restitution
				body.bottom = self.engine.height
				body.reinitialize(y=True)
			if body.left < 0:
				body.velocity.x *= -body.restitution
				body.left = 0
				body.reinitialize(x=True)
			elif body.right > self.engine.width:
				body.velocity.x *= -body.restitution
				body.right = self.engine.width
				body.reinitialize(x=True)

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
		# Find out which can be moved
		movable_one = one.mass > 0
		movable_two = two.mass > 0
		# Move bodies away
		if not movable_one and not movable_two:
			pass
		elif movable_one and not movable_two:
			one.move(vector)
		elif not movable_one and movable_two:
			two.move(-vector)
		elif movable_one and movable_two:
			one.move(vector / 2)
			two.move(-vector / 2)
