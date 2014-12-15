import pygame


class Animation(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		# Update sprites of animated entities
		for entity, animation in self.engine.entities.animations.items():
			if entity in self.engine.entities.sprites:
				animation.update()
				self.engine.entities.sprites[entity] = animation.get_image()
