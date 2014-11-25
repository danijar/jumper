import pygame
from vec import vec


class Movement(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		for entity in self.engine.entities.movements:
			movement = self.engine.entities.movements[entity]
			character = self.engine.entities.characters[entity]
			body = self.engine.entities.bodies[entity]
			# Get the sign on the axis, this is 1 for right and -1 for left
			sign = [-1, 1][movement.direction]
			new = None
			# Invert direction if at level boundaries
			if new is None:
				if body.left <= 0 or body.right >= self.engine.level.x:
					new = not movement.direction
			# Invert direction if there is a static obstacle
			if new is None:
				collider = pygame.Rect(body.left + (sign * character.speed), body.top, body.w, body.h)
				for other, other_body in self.engine.entities.bodies.items():
					if other == entity:
						continue
					if collider.colliderect(other_body):
						new = not movement.direction
						break
			# Invert direction if there is a gap
			if new is None:
				edge = 5
				collider = pygame.Rect(body.left + (sign * (body.width - edge)), body.top + body.height, body.w, body.h)
				for other, other_body in self.engine.entities.bodies.items():
					if other == entity:
						continue
					if collider.colliderect(other_body):
						break
				else:
					new = not movement.direction
			# Set movement
			if new is not None:
				movement.direction = new
			if movement.direction:
				body.velocity.x = character.speed
			else:
				body.velocity.x = -character.speed
