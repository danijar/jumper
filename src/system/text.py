import pygame


class Text(object):
	def __init__(self, engine):
		self.engine = engine
		self.font = pygame.font.Font('asset/font/source.ttf', 16)

	def update(self):
		# Render sprites
		screen = pygame.display.get_surface()
		text_offset = 0
		for entity in self.engine.entities.texts:
			# Evaluate lambda to get current content
			text = self.engine.entities.texts[entity]
			content = text.evaluate()
			sprite = self.font.render(content, True, (255, 255, 255))
			# Render text
			rect = sprite.get_rect()
			rect.top = text_offset
			text_offset = rect.bottom
			screen.blit(sprite, rect)
