import pygame

from component.animation import Animation as AnimationComponent


class Animation(object):
	def __init__(self, engine):
		self.engine = engine
		# Load animations
		AnimationComponent.load('asset/animation/player-idle.png', 3)
		AnimationComponent.load('asset/animation/player-hit.png', 3)

	def update(self):
		# Update sprites of animated entities
		for entity, animation in self.engine.entities.animations.items():
			if entity in self.engine.entities.sprites:
				animation.update()
				self.engine.entities.sprites[entity] = animation.get_image()
