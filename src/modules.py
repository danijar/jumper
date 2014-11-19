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
		delta = 1 / 60
		self.update_movement(delta)
		self.update_collision()
		self.update_velocity(delta)
		self.ensure_inside_window()
	def update_movement(self, delta):
		"""Move all bodies according to their velocity"""
		for body in self.system.entities.bodies.values():
			# Move body by velocity given in meters per second
			pixel_per_meter = 32
			body.move(body.velocity * delta * pixel_per_meter)
	def update_collision(self):
		"""Compute collisions between bodies"""
		for one, two in self.get_intersecting():
			# Create vectors to move objects out of intersection
			overlap = one.clip(two)
			point = vec(overlap.centerx, overlap.centery)
			away_one = (vec(one.centerx, one.centery) - point).normalize()
			away_two = (vec(two.centerx, two.centery) - point).normalize()
			# Scale by size of overlapping area
			away_one.x *= overlap.w / 2
			away_one.y *= overlap.h / 2
			away_two.x *= overlap.w / 2
			away_two.y *= overlap.h / 2
			# Scale by objects current velocity ratio
			velocity_sum = one.velocity.length() + two.velocity.length()
			away_one *= one.velocity.length() / max(velocity_sum, .001)
			away_two *= two.velocity.length() / max(velocity_sum, .001)
			# Move bodies away from each other
			one.move(away_one)
			two.move(away_two)
			# Swap velocities as a simplification to impulse calculation
			one.velocity, two.velocity = two.velocity, one.velocity
	def update_velocity(self, delta):
		"""Update velocity for the next frame"""
		for body in self.system.entities.bodies.values():
			# Bounce from window border
			if body.left < 0 or body.right > self.system.width:
				body.velocity.x *= -body.bounce.x
			if body.top < 0 or body.bottom > self.system.height:
				body.velocity.y *= -body.bounce.y
			# Apply gravity while in the air, on the
			# ground prevent from trying to move further
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
	def ensure_inside_window(self):
		"""Keep bodies inside window area"""
		for body in self.system.entities.bodies.values():
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
	def get_intersecting(self):
		"""Get all pairs of intersection bodies"""
		pairs = []
		bodies = list(self.system.entities.bodies.values())
		for i, one in enumerate(bodies):
			for j, two in enumerate(bodies[i + 1:]):
				if one.colliderect(two):
					pairs.append((one, two))
		return pairs

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
		text_offset = 0
		for entity in self.system.entities.sprites:
			sprite = self.system.entities.sprites.get(entity)
			body = self.system.entities.bodies.get(entity)
			text = self.system.entities.texts.get(entity)
			if body:
				screen.blit(sprite, body)
			elif text:
				rect = sprite.get_rect()
				rect.top = text_offset
				text_offset = rect.bottom
				screen.blit(sprite, rect)
