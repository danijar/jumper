import pygame
from system import System


class Window(object):
	def __init__(self, system):
		self.system = system
		# Set window properties and open it
		pygame.display.set_icon(pygame.image.load("asset/other/icon.png"))
		pygame.display.set_caption("Window")
		pygame.display.set_mode((system.width, system.height))
	def update(self):
		# Handle window events
		for event in pygame.event.get():
			# Allow application to quit
			if event.type == pygame.QUIT:
				self.system.running = False
			# User pressed a key
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.system.running = False
				elif event.key == pygame.K_c and event.mod & pygame.KMOD_LCTRL:
					self.system.running = False

class Player(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		keys = pygame.key.get_pressed()
		for entity in self.system.entities.players:
			player = self.system.entities.players[entity]
			if entity in self.system.entities.bodies:
				velocity = self.system.entities.bodies[entity].velocity
				if keys[player.controls['right']]:
					velocity[0] = player.speed
				if keys[player.controls['left']]:
					velocity[0] = -player.speed
				if keys[player.controls['jump']]:
					# Only jump if on the ground
					if self.system.entities.bodies[entity].bottom == self.system.height:	
						velocity[1] = -3.5 * player.speed
				self.system.entities.bodies[entity].velocity = velocity

class Body(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		# Update move properties
		for entity in self.system.entities.bodies:
			body = self.system.entities.bodies[entity]
			# Move body
			gravity = 6.0
			body.move([body.velocity[0], body.velocity[1] + gravity])
			# Bounce from window borders
			if body.left < 0 or body.right > self.system.width:
				body.velocity[0] *= -0.3
			if body.top < 0 or body.bottom > self.system.height:
				body.velocity[1] *= -0.3
			# Dump velocity to simulate frictions
			body.velocity[0] *= 0.99
			body.velocity[1] *= 0.99
			# Keep inside window area
			if body.top < 0:
				body.top = 0
				body.real[1] = body.y
			if body.bottom > self.system.height:
				body.bottom = self.system.height
				body.real[1] = body.y
			if body.left < 0:
				body.left = 0
				body.real[0] = body.x
			if body.right > self.system.width:
				body.right = self.system.width
				body.real[0] = body.x
			# Store result
			self.system.entities.bodies[entity] = body

class Sprite(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		# Render sprites
		screen = pygame.display.get_surface()
		screen.fill((0, 0, 0))
		for entity in self.system.entities.sprites:
			sprite = self.system.entities.sprites.get(entity)
			body = self.system.entities.bodies.get(entity)
			if body:
				screen.blit(sprite, body)
