import pygame, time


class Character(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		self.update_health()

	def update_health(self):
		for entity in self.engine.entities.characters.copy():
			character = self.engine.entities.characters[entity]
			# Character is dead
			if character.health < 1:
				# Detach from physics simulation and remove entity
				self.engine.entities.bodies[entity].detach()
				self.engine.entities.remove(entity)
