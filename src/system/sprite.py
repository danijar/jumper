import pygame


class Sprite(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		# Render sprites
		screen = pygame.display.get_surface()
		screen.fill((58, 112, 179))
		text_offset = 0
		for entity in self.engine.entities.sprites:
			sprite = self.engine.entities.sprites.get(entity)
			body = self.engine.entities.bodies.get(entity)
			text = self.engine.entities.texts.get(entity)
			if body:
				screen.blit(sprite, body)
