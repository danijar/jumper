import random
from operator import attrgetter
import pygame
from component.body import Body
from component.character import Character
from component.player import Player
from component.movement import Movement
from component.rail import Rail
from component.text import Text
from component.animation import Animated
from vec import vec


class Level(object):
	def __init__(self, engine):
		self.engine = engine
		self.load('asset/level/level.txt')

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

	def scale_height(self, entity, height):
		sprite = self.engine.entities.sprites[entity]
		size = vec(sprite.get_width(), sprite.get_height())
		size *= height / sprite.get_height()
		self.scale(entity, size)

	def move(self, entity, offset):
		body = self.engine.entities.bodies[entity]
		body.real += offset
		body.reinitialize()

	def add_enemy(self, entity):
		if entity is None:
			entity = self.engine.entities.create()
		# Load default sprite
		if entity not in self.engine.entities.sprites:
			self.engine.entities.sprites[entity] = pygame.image.load("asset/texture/enemy.png")
		# Attach body and tweak parameters
		if entity not in self.engine.entities.bodies:
			self.engine.entities.bodies[entity] = Body(self.engine.entities.sprites[entity].get_rect())
		body = self.engine.entities.bodies[entity]
		body.mass = 70.0
		body.friction.x = 10.0
		# Attach default character component
		character = Character()
		character.speed = 1.0
		character.health = 2
		self.engine.entities.characters[entity] = character
		# Attach movement behavior
		self.engine.entities.movements[entity] = Movement()
		# Animations
		self.engine.entities.animations[entity] = Animated()
		return entity

	def add_player(self, number=1, entity=None, controls=None):
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
		# Attach default character component
		character = Character()
		self.engine.entities.characters[entity] = character
		# Attach player component and override provided controls
		player = Player()
		player.number = number
		if controls:
			player.controls = controls
		self.engine.entities.players[entity] = player
		# Attach text component for health and ammo display
		evaluate = lambda: 'Player {0} has {1} lifes left.'.format(number, character.health)
		self.engine.entities.texts[entity] = Text(evaluate)
		# Animations
		self.engine.entities.animations[entity] = Animated()
		return entity
	
	def load(self, path):
		grid = 48
		rail = None
		position = vec()
		with open(path) as lines:
			for y, line in enumerate(lines):
				for x, symbol in enumerate(line[:-1]):
					position = vec(x * grid, y * grid)
					# Remember level boundaries
					if position.x + grid > self.engine.level.x:
						self.engine.level.x = position.x + grid
					if position.y + grid > self.engine.level.y:
						self.engine.level.y = position.y + grid
					# End rail when tile is neither rail nor platform
					if rail is not None and symbol not in '-#':
						rail.right = position.x - 1
						rail = None
					# Platform
					if symbol == '#':
						entity = self.create_body("asset/texture/platform.png", position)
						self.scale(entity, grid)
						if rail is not None:
							rail.platforms.append(entity)
					# First player
					elif symbol == '1':
						entity = self.create_body("asset/texture/player.png", position)
						self.scale_height(entity, grid)
						self.add_player(1, entity)
					# Second player
					elif symbol == '2':
						entity = self.create_body("asset/texture/player.png", position)
						self.scale_height(entity, grid)
						self.add_player(2, entity, {
							'up': pygame.K_UP,
							'left': pygame.K_LEFT,
							'down': pygame.K_DOWN,
							'right': pygame.K_RIGHT,
							'jump': pygame.K_UP,
							'attack': pygame.K_RETURN
						})
					# Add enemy
					elif symbol == 'A':
						entity = self.create_body("asset/texture/enemy.png", position)
						self.scale(entity, vec(grid / 1.5, grid))
						self.move(entity, vec(grid / 1.5, 0))
						self.add_enemy(entity)
					# Rail for moving platform
					elif symbol == '-' and rail is None:
						entity = self.engine.entities.create()
						rail = Rail()
						rail.left = position.x
						self.engine.entities.rails[entity] = rail
					# Randomly fill with boxes
					elif random.random() < 0.04:
						entity = self.create_body("asset/texture/box.png", position, 25.0)
						self.scale(entity, 35)
					# Randomly fill with rocks
					elif random.random() < 0.04:
						length = int(30 + (20 * random.random()))
						entity = self.create_body("asset/texture/rock.png", position, length * length)
						self.scale(entity, length)
				# End rail when line ends
				if rail is not None:
					rail.right = position.x - 1
					rail = None

	def update(self):
		delta = 1 / 60
		self.scroll()
		self.rail(delta)

	def scroll(self):
		# Find player one
		if len(self.engine.entities.players) < 1:
			return
		entity = min(self.engine.entities.players.items(), key=lambda x: x[1].number)[0]
		# Scroll level to center player
		body = self.engine.entities.bodies[entity]
		self.engine.scroll = vec(body.center) - (vec(self.engine.width, self.engine.height) / 2)
		# Clamp scroll to level borders
		if self.engine.scroll.x < 0:
			self.engine.scroll.x = 0
		elif self.engine.scroll.x > self.engine.level.x - self.engine.width:
			self.engine.scroll.x = self.engine.level.x - self.engine.width
		if self.engine.scroll.y < 0:
			self.engine.scroll.y = 0
		elif self.engine.scroll.y > self.engine.level.y - self.engine.height:
			self.engine.scroll.y = self.engine.level.y - self.engine.height

	def rail(self, delta):
		for rail in self.engine.entities.rails.values():
			if len(rail.platforms) < 1:
				continue
			first = self.engine.entities.bodies[rail.platforms[0]]
			last = self.engine.entities.bodies[rail.platforms[-1]]
			if first.left < rail.left:
				rail.direction = True
			elif last.right > rail.right:
				rail.direction = False
			for entity in rail.platforms:
				body = self.engine.entities.bodies[entity]
				offset = delta * rail.speed
				if not rail.direction:
					offset *= -1
				body.move(vec(offset, 0))
