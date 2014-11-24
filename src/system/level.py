import random
import pygame
from component.body import Body
from component.player import Player
from vec import vec


class Rail(object):
	def __init__(self):
		self.left = 0.0
		self.right = 0.0
		self.direction = True
		self.platforms = []
		self.speed = 75.0


class Level(object):
	def __init__(self, engine):
		self.engine = engine
		self.rails = []
		self.load('level/level.txt')

	def create_body(self, texture, position=vec(0), mass=0):
		entity = self.engine.entities.create()
		self.engine.entities.sprites[entity] = pygame.image.load(texture)
		body = Body(self.engine.entities.sprites[entity].get_rect())
		body.set(position)
		body.mass = mass
		self.engine.entities.bodies[entity] = body
		return entity

	def scale(self, entity, size):
		size = vec(size)
		sprite = self.engine.entities.sprites[entity]
		sprite = pygame.transform.scale(sprite, size.list())
		self.engine.entities.sprites[entity] = sprite
		body = self.engine.entities.bodies[entity]
		body.h = sprite.get_rect().h
		body.w = sprite.get_rect().w

	def move(self, entity, offset):
		body = self.engine.entities.bodies[entity]
		body.real += offset
		body.reinitialize()

	def add_player(self, entity=None, controls=None):
		if entity is None:
			entity = self.engine.entities.create()
		# Load default sprite
		if entity not in self.engine.entities.sprites:
			self.engine.entities.sprites[entity] = pygame.image.load("asset/texture/player.png")
		# Attach body and tweak parameters
		if entity not in self.engine.entities.bodies:
			self.engine.entities.bodies[entity] = Body(self.engine.entities.sprites[entity].get_rect())
		body = self.engine.entities.bodies[entity]
		body.mass = 70.0
		body.friction.x = 10.0
		body.restitution = 0.0
		# Attach player component and override provided controls
		player = Player()
		if controls:
			player.controls = controls
		self.engine.entities.players[entity] = player
		return entity
	
	def load(self, path):
		grid = 48
		rail = None
		with open(path) as lines:
			for y, line in enumerate(lines):
				for x, symbol in enumerate(line):
					position = vec(x * grid, y * grid)
					# Platform
					if symbol == '#':
						entity = self.create_body("asset/texture/platform.png", position)
						self.scale(entity, grid)
						if rail is not None:
							rail.platforms.append(entity)
					# First player
					elif symbol == 'P':
						entity = self.create_body("asset/texture/player.png", position)
						self.scale(entity, vec(grid / 1.5, grid))
						self.move(entity, vec(grid / 1.5, 0))
						self.add_player(entity)
					# Second player
					elif symbol == 'Q':
						entity = self.create_body("asset/texture/player-2.png", position)
						self.scale(entity, vec(grid / 1.5, grid))
						self.move(entity, vec(grid / 1.5, 0))
						self.add_player(entity, {
							'up': pygame.K_UP,
							'left': pygame.K_LEFT,
							'down': pygame.K_DOWN,
							'right': pygame.K_RIGHT,
							'jump': pygame.K_UP
						})
					# Rail for moving platform
					# Currently, this assumes that rails end in the same line
					elif symbol == '-' and rail is None:
						rail = Rail()
						rail.left = position.x
					elif symbol == ' ' and rail is not None:
						rail.right = position.x - 1
						self.rails.append(rail)
						rail = None
					# Randomly fill with ballons
					elif random.random() < 0.10:
						entity = self.create_body("asset/texture/balloon.png", position, 1.0)
						self.scale(entity, 35)
					# Randomly fill with rocks
					elif random.random() < 0.07:
						length = int(30 + (20 * random.random()))
						entity = self.create_body("asset/texture/rock.png", position, length * length)
						self.scale(entity, length)

	def update(self):
		delta = 1 / 60

		self.platform(delta)

	def platform(self, delta):
		for rail in self.rails:
			first = self.engine.entities.bodies[rail.platforms[0]]
			last = self.engine.entities.bodies[rail.platforms[-1]]
			if first.left < rail.left:
				#body.left = rail.left
				#body.reinitialize()
				rail.direction = True
			elif last.right > rail.right:
				#body.right = rail.right
				#body.reinitialize()
				rail.direction = False
			for entity in rail.platforms:
				body = self.engine.entities.bodies[entity]
				offset = delta * rail.speed
				if not rail.direction:
					offset *= -1
				body.move(vec(offset, 0))