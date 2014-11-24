import pygame


class Text(object):
	def __init__(self, engine):
		self.engine = engine
		self.font = pygame.font.Font('asset/font/source.ttf', 16)

	def update(self):
		# Update sprites
		for entity in self.engine.entities.texts:
			text = self.engine.entities.texts[entity]
			sprite = self.font.render(text, True, (255, 255, 255))
			self.engine.entities.sprites[entity] = sprite
