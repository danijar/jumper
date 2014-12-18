import pygame


class Interface(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		# Render sprites
		screen = pygame.display.get_surface()
		text_offset = 30
		for entity, text in self.engine.entities.interfaces.items():
			# Evaluate lambda to get current sprite
			sprite = text.evaluate()
			# Position can be returned as second value
			if isinstance(sprite, tuple):
				sprite, rect = sprite
			# Otherwise, position below each other
			else:
				rect = sprite.get_rect()
				rect.top = text_offset
				text_offset = rect.bottom
			# Render text
			screen.blit(sprite, rect)
