import random
import pygame
from properties import Body, Player
from vec import vec


def initialize(system):
	def create_body(texture):
		entity = system.entities.create()
		system.entities.sprites[entity] = pygame.image.load(texture)
		system.entities.bodies[entity] = Body(system.entities.sprites[entity].get_rect())
		return entity

	def scale(entity, length):
		sprite = system.entities.sprites[entity]
		sprite = pygame.transform.scale(sprite, [length, length])
		system.entities.sprites[entity] = sprite
		system.entities.bodies[entity] = Body(sprite.get_rect())

	def create_boxes(amount=32):
		for i in range(amount):
			entity = create_body("asset/texture/box.png")
			# Scale randomly
			length = int(30 + (20 * random.random()))
			scale(entity, length)
			# Add body, center position and push them around
			body = system.entities.bodies[entity]
			body.bottom = system.height - 50
			body.centerx = int(system.width / 2)
			body.real = vec(body.x, body.y)
			body.velocity.x = 40 * (random.random() - .5)
			body.velocity.y = -(20 + 20 * random.random())

	def create_platforms(amount=32):
		for i in range(amount):
			entity = create_body("asset/texture/platform.png")
			# Set scale
			scale(entity, 40)
			# Position randomly in bottom half of the window
			body = system.entities.bodies[entity]
			body.left = int(random.random() * (system.width -body.w))
			half_height = system.height / 2
			body.top = half_height + int(random.random() * (half_height - body.h))
			body.real = vec(body.x, body.y)
			# Make static
			body.mass = 0

	def create_player(up=None, left=None, down=None, right=None, jump=None):
		entity = system.entities.create()
		system.entities.sprites[entity] = pygame.image.load("asset/texture/player.png")
		system.entities.players[entity] = Player()
		# Add body and place at bottom center of window
		body = Body(system.entities.sprites[entity].get_rect())
		body.friction.x = 3.0
		body.bottom = system.height
		body.centerx = int(system.width / 2)
		body.real = vec(body.x, body.y)
		body.restitution = 0.1
		system.entities.bodies[entity] = body
		# Override provided controls
		if up: controls['up'] = up
		if left: controls['left'] = left
		if down: controls['down'] = down
		if right: controls['right'] = right
		if jump: controls['jump'] = jump

	create_boxes(5)
	create_platforms(5)
	create_player()
