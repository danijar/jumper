import random
import pygame
from component.body import Body
from component.player import Player
from vec import vec


def initialize(engine):
	def create_body(texture):
		entity = engine.entities.create()
		engine.entities.sprites[entity] = pygame.image.load(texture)
		engine.entities.bodies[entity] = Body(engine.entities.sprites[entity].get_rect())
		return entity

	def scale(entity, length):
		sprite = engine.entities.sprites[entity]
		sprite = pygame.transform.scale(sprite, [length, length])
		engine.entities.sprites[entity] = sprite
		engine.entities.bodies[entity] = Body(sprite.get_rect())

	def add_platforms(amount=5):
		for i in range(amount):
			entity = create_body("asset/texture/platform.png")
			# Set scale
			scale(entity, 40)
			# Position randomly in bottom half of the window
			body = engine.entities.bodies[entity]
			body.left = int(random.random() * (engine.width -body.w))
			half_height = engine.height / 2
			body.top = half_height + int(random.random() * (half_height - body.h))
			body.real = vec(body.x, body.y)
			# Make static
			body.mass = 0

	def add_rocks(amount=5):
		for i in range(amount):
			entity = create_body("asset/texture/rock.png")
			# Scale randomly
			length = int(30 + (20 * random.random()))
			scale(entity, length)
			# Add body, center position and push them around
			body = engine.entities.bodies[entity]
			body.mass = length * length
			body.bottom = engine.height - 50
			body.centerx = int(engine.width / 2)
			body.real = vec(body.x, body.y)
			body.velocity.x = 40 * (random.random() - .5)
			body.velocity.y = -(20 + 20 * random.random())

	def add_balloons(amount=5):
		for i in range(amount):
			entity = create_body("asset/texture/balloon.png")
			# Scale randomly
			scale(entity, 35)
			# Add body, center position and push them around
			body = engine.entities.bodies[entity]
			body.mass = 1.0
			body.bottom = engine.height - 50
			body.centerx = int(engine.width / 2)
			body.real = vec(body.x, body.y)
			body.velocity.x = 40 * (random.random() - .5)
			body.velocity.y = -(20 + 20 * random.random())

	def add_player(up=None, left=None, down=None, right=None, jump=None):
		entity = engine.entities.create()
		engine.entities.sprites[entity] = pygame.image.load("asset/texture/player.png")
		engine.entities.players[entity] = Player()
		# Add body and place at bottom center of window
		body = Body(engine.entities.sprites[entity].get_rect())
		body.mass = 70.0
		body.friction.x = 10.0
		body.bottom = engine.height
		body.centerx = int(engine.width / 2)
		body.real = vec(body.x, body.y)
		body.restitution = 0.0
		engine.entities.bodies[entity] = body
		# Override provided controls
		if up:
			controls['up'] = up
		if left:
			controls['left'] = left
		if down:
			controls['down'] = down
		if right:
			controls['right'] = right
		if jump:
			controls['jump'] = jump

	add_platforms(7)
	add_rocks(5)
	add_balloons(5)
	add_player()
