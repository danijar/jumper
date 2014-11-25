import pygame


class Movement(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		for entity in self.engine.entities.movements:
			movement = self.engine.entities.movements[entity]
			character = self.engine.entities.characters[entity]
			body = self.engine.entities.bodies[entity]
			# Get the sign on the axis, this is 1 for right and -1 for left
			direction = [-1, 1][movement.direction]
			# Invert direction if there is a static obstacle
			collider = pygame.Rect(body.left + (direction * character.speed), body.top, body.w, body.h)
			for other, other_body in self.engine.entities.bodies.items():
				if other == entity:
					continue
				colliding = collider.colliderect(other_body)
				static = other_body.mass == 0
				heavy = body.mass < other_body.mass / 2
				if colliding and (static or heavy):
					movement.direction = not movement.direction
					break
			# Invert direction if there is a gap
			else:
				edge = 5
				collider = pygame.Rect(body.left + (direction * (body.width - edge)), body.top + body.height, body.w, body.h)
				for other, other_body in self.engine.entities.bodies.items():
					if other == entity:
						continue
					colliding = collider.colliderect(other_body)
					static = other_body.mass == 0
					heavy = body.mass < other_body.mass / 2
					if colliding and (static or heavy):
						break
				else:
					movement.direction = not movement.direction
			# Set movement
			if movement.direction:
				body.velocity.x = character.speed
			else:
				body.velocity.x = -character.speed
