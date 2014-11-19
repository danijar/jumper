import os
import pygame
from system import System
from vec import vec


class Window(object):
	def __init__(self, system):
		self.system = system
		# Set window properties and open it
		os.environ['SDL_VIDEO_CENTERED'] = '1'
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
			body = self.system.entities.bodies[entity]
			if body:
				if keys[player.controls['right']]:
					body.velocity.x = player.speed
				if keys[player.controls['left']]:
					body.velocity.x = -player.speed
				if keys[player.controls['jump']]:
					# Only jump if on the ground
					if body.bottom == self.system.height:	
						body.velocity.y = -2.5 * player.speed

class Body(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		# Update move properties
		for entity in self.system.entities.bodies:
			body = self.system.entities.bodies[entity]
			# Move body
			# Velocity is in meters per second so convert to pixels per frame
			delta = 1 / 60
			pixel_per_meter = 32
			body.move(body.velocity * delta * pixel_per_meter)
			# Bounce from window borders
			if body.left < 0 or body.right > self.system.width:
				body.velocity.x *= -body.bounce.x
			if body.top < 0 or body.bottom > self.system.height:
				body.velocity.y *= -body.bounce.y
			# Apply gravity while in the air
			gravity = 15.0
			if body.bottom < self.system.height:
				body.velocity.y += gravity * delta
			else:
				body.velocity.y = min(body.velocity.y, 0)
			# Dump velocity to simulate air drag
			body.velocity.x *= max(1 - body.dumping.x, 0)
			body.velocity.y *= max(1 - body.dumping.y, 0)
			# Simulate friction when on the ground
			if body.bottom >= self.system.height:
				body.velocity.x *= max(1 - body.friction.x, 0)
				body.velocity.y *= max(1 - body.friction.y, 0)
			# Keep inside window area
			if body.top < 0:
				body.top = 0
				body.reinitialize_y()
			elif body.bottom > self.system.height:
				body.bottom = self.system.height
				body.reinitialize_y()
			if body.left < 0:
				body.left = 0
				body.reinitialize_x()
			elif body.right > self.system.width:
				body.right = self.system.width
				body.reinitialize_x()

class Text(object):
	def __init__(self, system):
		self.system = system
		self.font = pygame.font.Font('asset/font/source.ttf', 16)
	def update(self):
		# Update sprites
		for entity in self.system.entities.texts:
			text = self.system.entities.texts[entity]
			sprite = self.font.render(text, True, (255, 255, 255))
			self.system.entities.sprites[entity] = sprite

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
			text = self.system.entities.texts.get(entity)
			if body:
				screen.blit(sprite, body)
			elif text:
				screen.blit(sprite, sprite.get_rect())
