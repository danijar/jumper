import math
import pygame
from vec import vec


class Body(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		"""Update all sub systems"""
		delta = 1 / 60
		# Standing objects must be determined as first step for the other
		# physics calculations and also at the end so that other systems read
		# the resulting state.
		self.update_standings()
		self.update_movements(delta)
		self.update_collisions()
		self.update_insides()
		self.update_velocities(delta)
		self.update_standings()

	def update_movements(self, delta):
		"""Move all bodies according to their velocity"""
		for body in self.engine.entities.bodies.values():
			# Move body by velocity given in meters per second
			pixels_per_meter = 32
			body.move(body.velocity * delta * pixels_per_meter)

	def update_standings(self):
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
			# Update standing property
			body.standing = len(body.underneaths) > 0

	def update_collisions(self):
		"""Resolve collisions between bodies"""
		pairs = self.get_intersecting()
		for one, two in pairs:
			# Resolve collision along the axis with smaller intersection
			overlap = one.clip(two)
			overlap.normalize()
			# Resolve shorter direction
			if abs(overlap.w) < abs(overlap.h):
				self.horizontal_collision(one, two, overlap)
			else:
				self.vertical_collision(one, two, overlap)

	def update_velocities(self, delta):
		"""Update velocity for the next frame"""
		for body in self.engine.entities.bodies.values():
			# Skip static bodies
			if body.mass == 0:
				continue
			# Apply gravity while in the air, on the ground prevent from
			# trying to move further.
			gravity = 9.81
			if not body.standing:
				body.velocity.y += gravity * delta
			else:
				body.velocity.y = min(body.velocity.y, 0)
			# Dump velocity to simulate air drag
			body.velocity.x *= max(1 - body.dumping.x, 0)
			body.velocity.y *= max(1 - body.dumping.y, 0)
			# Simulate friction when on the ground
			if body.standing:
				body.velocity.x *= max(1 - body.friction.x, 0)
				body.velocity.y *= max(1 - body.friction.y, 0)

	def update_insides(self):
		"""Keep bodies inside window area"""
		for body in self.engine.entities.bodies.values():
			# Skip static bodies
			if body.mass == 0:
				continue
			# Bounce from level border. This includes both inverting velocity
			# relative to the restitution factor, and ensuring the body's
			# position to be inside.
			if body.top < 0:
				body.top = 0
				body.reinitialize(y=True)
				body.velocity.y *= -body.restitution
			elif body.bottom > self.engine.level.y:
				body.bottom = self.engine.level.y
				body.reinitialize(y=True)
				body.velocity.y *= -body.restitution
			if body.left < 0:
				body.left = 0
				body.reinitialize(x=True)
				body.velocity.x *= -body.restitution
			elif body.right > self.engine.level.x:
				body.right = self.engine.level.x
				body.reinitialize(x=True)
				body.velocity.x *= -body.restitution

	def get_intersecting(self):
		"""Get all pairs of intersection bodies"""
		pairs = []
		bodies = list(self.engine.entities.bodies.values())
		for i, one in enumerate(bodies):
			# Second loop only has to traverse later bodies, previous ones
			# have already be seen ín form of the inverse pair.
			for j, two in enumerate(bodies[i + 1:]):
				# Two static bodies can't collide, so skip this case. Even if
				# they do, it's intended by level design.
				if one.mass == 0 and two.mass == 0:
					continue
				# Determine if areas of the bodies intersect
				if one.colliderect(two):
					pairs.append((one, two))
		return pairs

	def horizontal_collision(self, one, two, overlap):
		# Move bodies apart
		way = -overlap.w if one.x < two.x else overlap.w
		self.move_apart(one, two, vec(way, 0))
		
	def vertical_collision(self, one, two, overlap):
		above, below = (one, two) if one.y < two.y else (two, one)
		# Move bodies apart
		way = -overlap.h if one.y < two.y else overlap.h
		self.move_apart(one, two, vec(0, way))
		# Stack dynamic bodies but stop movement at static ones
		if above.mass > 0:
			above.underneaths.add(below)
			below.ontops.add(above)
		else:
			below.velocity.y = max(below.velocity.y, 0)
		
	def move_apart(self, one, two, vector):
		"""Move two intersecting bodies apart, taking their mass into account"""
		# Find out which bodies can be moved, a mass of zero means static
		movable_one = one.mass > 0
		movable_two = two.mass > 0
		# Move bodies away
		if not movable_one and not movable_two:
			# Allow two static bodies to instersect
			pass
		elif movable_one and not movable_two:
			# Second body is static, so first must move the whole distance
			one.move(vector)
		elif not movable_one and movable_two:
			# First body is static, so second must move the whole distance
			two.move(-vector)
		elif movable_one and movable_two:
			# Two dynamic bodies must be moved relative to their mass ratio
			overall_mass = one.mass + two.mass
			ratio_one = one.mass / overall_mass
			ratio_two = two.mass / overall_mass
			# Reduce this effect by weighting it with equipartition
			amount = 0.7
			ratio_one = amount * ratio_one + (1 - amount) * 0.5
			ratio_two = amount * ratio_two + (1 - amount) * 0.5
			# Move bodies
			one.move(+vector * ratio_two)
			two.move(-vector * ratio_one)
