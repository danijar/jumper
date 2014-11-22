import os, math
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
		self.update_input()
	def update_input(self):
		"""Handle movement from user input"""
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
					if body.on_ground:
						body.velocity.y = -2.5 * player.speed

class Body(object):
	def __init__(self, system):
		self.system = system
	def update(self):
		delta = 1 / 60
		self.update_movement(delta)
		self.update_collision()
		self.update_velocity(delta)
		self.update_inside_window()
		self.update_on_ground()
	def update_movement(self, delta):
		"""Move all bodies according to their velocity"""
		for body in self.system.entities.bodies.values():
			# Move body by velocity given in meters per second
			pixel_per_meter = 32
			body.move(body.velocity * delta * pixel_per_meter)
	def update_collision(self):
		"""Resolve collisions between bodies"""
		pairs = self.get_intersecting()
		for one, two in pairs:
			# Use shortest line between center of bodies as collision normal
			normal = (vec(two.center) - vec(one.center)).normalize()
			# Compute relative velocity between bodies along collision normal
			velocity = two.velocity - one.velocity
			contact_velocity = velocity.dot(normal)
			# Don't resolve if bodies are already separating
			if contact_velocity > 0:
				continue
			# Use minimum restitution for both bodies
			restitution = min(one.restitution, two.restitution)
			# Calculate impulse
			amount = -(1 + restitution) * contact_velocity
			amount /= one.mass + two.mass
			impulse = normal * amount
			# Apply impulse
			one.velocity -= impulse * (1 / one.mass)
			two.velocity += impulse * (1 / two.mass)
		for one, two in pairs:
			# Prevent objects from moving into each other
			self.compensate_peneration(one, two)
	def update_velocity(self, delta):
		"""Update velocity for the next frame"""
		for body in self.system.entities.bodies.values():
			# Bounce from window border
			if body.left < 0 or body.right > self.system.width:
				body.velocity.x *= -body.restitution
			if body.top < 0 or body.bottom > self.system.height:
				body.velocity.y *= -body.restitution
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
			if body.on_ground:
				body.velocity.x *= max(1 - body.friction.x, 0)
				body.velocity.y *= max(1 - body.friction.y, 0)
	def update_inside_window(self):
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
	def update_on_ground(self):
		"""Check if players are standing on the ground"""
		for entity in self.system.entities.bodies:
			body = self.system.entities.bodies[entity]
			# Reset property to check again every frame
			body.on_ground = False
			# Early exit if body is at bottom of window
			if body.bottom == self.system.height:
				body.on_ground = True
				continue
			# Check if another body intersects with the body's bottom area
			area = pygame.Rect(body.left, body.bottom - 0.2, body.w, 0.4)
			for other in self.system.entities.bodies:
				if other == entity:
					continue
				if self.system.entities.bodies[other].colliderect(area):
					body.on_ground = True
					break
	def get_intersecting(self):
		"""Get all pairs of intersection bodies"""
		pairs = []
		bodies = list(self.system.entities.bodies.values())
		for i, one in enumerate(bodies):
			for j, two in enumerate(bodies[i + 1:]):
				if one.colliderect(two):
					pairs.append((one, two))
		return pairs
	def compensate_peneration(self, one, two):
		"""Compensate floating point errors that make objects move into each
		other by manually moving them apart"""
		# Use shortest line between center of bodies as collision normal
		# This could be reused from the parent function update_collision()
		normal = (vec(two.center) - vec(one.center)).normalize()
		# Approximate penetration
		overlap = two.clip(one)
		penetration = min(overlap.w, overlap.h) * math.sqrt(2)
		# Ignore small amount of penetration
		penetration -= 0.01
		if penetration < 0:
			return
		# Calculate correction
		amount = 0.2
		correction = normal * amount * (penetration / (1 / one.mass) + (1 / two.mass))
		#print(penetration, correction)
		# Apply correction
		one.real -= correction * (1 / one.mass)
		two.real += correction * (1 / two.mass)

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
