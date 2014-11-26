import pygame
from vec import vec


class Movement(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		"""Update all sub systems"""
		self.update_levels()
		self.update_obstacles()
		self.update_gaps()
		self.update_apply()

	def update_levels(self):
		"""Change directions at level bounds"""
		for entity, movement in self.engine.entities.movements.items():
			# Fetch components
			character = self.engine.entities.characters.get(entity)
			body = self.engine.entities.bodies.get(entity)
			if not body or not character:
				continue
			# Invert direction if at level boundaries
			if body.left <= 0 or body.right >= self.engine.level.x:
				movement.changed = True

	def update_obstacles(self):
		"""Change directions when facing a gap"""
		for entity, movement in self.engine.entities.movements.items():
			# Fetch components
			character = self.engine.entities.characters.get(entity)
			body = self.engine.entities.bodies.get(entity)
			if not body or not character:
				continue
			# Invert direction if there is a static obstacle
			sign = [-1, 1][movement.direction]
			infront = pygame.Rect(
				body.left + (sign * character.speed),
				body.top,
				body.w,
				body.h - 1
			)
			# Invert direction if there is an obstacle
			for other, other_body in self.engine.entities.bodies.items():
				if other == entity:
					continue
				if infront.colliderect(other_body):
					movement.changed = True
					break

	def update_gaps(self):
		"""Change directions when facing a gap"""
		for entity, movement in self.engine.entities.movements.items():
			# Fetch components
			character = self.engine.entities.characters.get(entity)
			body = self.engine.entities.bodies.get(entity)
			if not body or not character:
				continue
			# Area where ground should be for walking
			sign = [-1, 1][movement.direction]
			edge_distance = 5
			ground = pygame.Rect(
				body.left + (sign * (body.width - edge_distance)),
				body.top + body.height,
				body.w,
				body.h
			)
			# Invert direction if there is a gap
			for other, other_body in self.engine.entities.bodies.items():
				if other == entity:
					continue
				if other_body.colliderect(ground):
					break
			else:
				movement.changed = True

	def update_apply(self):
		"""Apply movement. Also swap directions of components that have been
		marked"""
		for entity, movement in self.engine.entities.movements.items():
			# Apply direction change
			if movement.changed:
				movement.changed = False
				movement.direction = not movement.direction
			# Fetch components
			body = self.engine.entities.bodies.get(entity)
			character = self.engine.entities.characters.get(entity)
			if not body or not character:
				continue
			# Apply movement
			sign = [-1, 1][movement.direction]
			body.velocity.x = sign * character.speed
