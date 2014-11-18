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
			if entity in self.system.entities.movements:
				direction = [0, 0]
				if keys[player.controls['right']]:
					direction[0] += 1
				if keys[player.controls['left']]:
					direction[0] -= 1
				if keys[player.controls['down']]:
					direction[1] += 1
				if keys[player.controls['up']]:
					direction[1] -= 1
				self.system.entities.movements[entity].direction = direction

class Movement(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		# Update move properties
		for entity in self.system.entities.movements:
			movement = self.system.entities.movements.get(entity)
			body = self.system.entities.bodies.get(entity)
			if body:
				# Move in current direction with current speed
				way = [x * movement.speed for x in movement.direction]
				body.move(way)
				# Bounce from window borders
				if body.left < 0 or body.right > self.system.width:
					movement.direction[0] *= -1
				if body.top < 0 or body.bottom > self.system.height:
					movement.direction[1] *= -1
				# Keep inside window area
				if body.top < 0:
					body.top = 0
					body.float_y = body.y
				if body.bottom > self.system.height:
					body.bottom = self.system.height
					body.float_y = body.y
				if body.left < 0:
					body.left = 0
					body.float_x = body.x
				if body.right > self.system.width:
					body.right = self.system.width
					body.float_x = body.x
				# Store result
				self.system.entities.movements[entity] = movement
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
