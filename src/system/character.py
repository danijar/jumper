import pygame, time
from vec import vec


class Character(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		self.update_health()

	def update_health(self):
		bounce = 0.2
		for entity in self.engine.entities.characters.copy():
			character = self.engine.entities.characters[entity]
			# Update enemies
			if entity not in self.engine.entities.players:
				body = self.engine.entities.bodies[entity]
				# Hit enemies when objects fall on them
				for other in body.ontops.copy():
					character.health -= 1
					other.velocity.y -= body.mass * bounce
					body.ontops.remove(other)
					other.underneaths.remove(body)
				# Hit players when enemies walk into them
				for other_entity in self.engine.entities.players:
					if other_entity == entity:
						continue
					other_body = self.engine.entities.bodies[other_entity]
					other_character = self.engine.entities.characters[other_entity]
					# Check if overlapping with player body, allow feet
					collider = pygame.Rect(other_body.left - 1, other_body.top, other_body.w + 2, other_body.h - 1)
					if body.colliderect(collider):
						other_character.health -= 1
						normal = (vec(other_body) - vec(body) + vec(0, -20)).normalize()
						other_body.velocity += normal * body.mass * bounce
			# Remove dead characters
			if character.health < 1:
				# Detach from physics simulation and remove entity
				self.engine.entities.bodies[entity].detach()
				self.engine.entities.remove(entity)
