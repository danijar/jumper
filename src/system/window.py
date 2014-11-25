import os
import pygame


class Window(object):
	def __init__(self, engine):
		self.engine = engine
		# Set window properties and open it
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pygame.display.set_icon(pygame.image.load("asset/other/icon.png"))
		pygame.display.set_caption("Window")
		pygame.display.set_mode((engine.width, engine.height))

	def update(self):
		# Handle window events
		for event in pygame.event.get():
			# Allow application to quit
			if event.type == pygame.QUIT:
				self.engine.running = False
			# User pressed a key
			elif event.type == pygame.KEYDOWN:
				# Allow systems to listen to keydown events
				self.engine.events.fire('keydown', event.key)
				# Exit on Escape
				if event.key == pygame.K_ESCAPE:
					self.engine.running = False
				# Exit on Ctrl-Z
				elif event.key == pygame.K_c and event.mod & pygame.KMOD_LCTRL:
					self.engine.running = False
