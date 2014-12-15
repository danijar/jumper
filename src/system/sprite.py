import pygame


class Sprite(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		# Render sprites
		screen = pygame.display.get_surface()
		screen.fill((93, 116, 126))
		text_offset = 0
		for entity in self.engine.entities.sprites:
			# Get properties
			sprite = self.engine.entities.sprites.get(entity)
			body = self.engine.entities.bodies.get(entity)
			animation = self.engine.entities.animations.get(entity)
			if not body:
				continue
			# Find position in level
			x = body.left - self.engine.scroll.x
			y = body.top - self.engine.scroll.y
			if animation and animation.running:
				# Render sprite animation frame
				size = self.engine.entities.sprites[entity].get_size()
				frame = animation.get_frame()
				frame = pygame.transform.scale(frame, size)
				screen.blit(frame, (x, y))
			else:
				# Render static sprite property
				screen.blit(sprite, (x, y))
