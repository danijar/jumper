import pygame


class Text(object):
	def __init__(self, engine):
		self.engine = engine
		self.font = pygame.font.Font('asset/font/source.ttf', 16)

	def update(self):
		# Update sprites
		for entity in self.engine.entities.texts:
			text = self.engine.entities.texts[entity]
			text.content = text.evaluate()
			sprite = self.font.render(text.content, True, (255, 255, 255))
			self.engine.entities.sprites[entity] = sprite
