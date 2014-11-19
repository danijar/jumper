import random
import pygame
from properties import Body, Player
from vec import vec


def initialize(system):
	def create_ball():
		entity = system.entities.create()
		system.entities.sprites[entity] = pygame.image.load("asset/texture/circle.png")
		system.entities.bodies[entity] = Body(system.entities.sprites[entity].get_rect())
		return entity

	def create_balls(amount=32):
		for i in range(amount):
			entity = create_ball()
			# Sprite
			sprite = system.entities.sprites[entity]
			length = int(30 + (20 * random.random()))
			sprite = pygame.transform.scale(sprite, [length, length])
			system.entities.sprites[entity] = sprite		
			# Add body, center position and push them around
			body = Body(sprite.get_rect())
			body.bottom = system.height
			body.centerx = int(system.width / 2)
			body.real = vec(body.x, body.y)
			body.velocity.x = 40 * (random.random() - .5)
			body.velocity.y = -(20 + 20 * random.random())
			system.entities.bodies[entity] = body

	def create_player(up=None, left=None, down=None, right=None, jump=None):
		entity = system.entities.create()
		system.entities.sprites[entity] = pygame.image.load("asset/texture/player.png")
		system.entities.players[entity] = Player()
		# Add body and place at bottom center of window
		body = Body(system.entities.sprites[entity].get_rect())
		body.friction.x = 3.0 # 0.05
		body.bottom = system.height
		body.centerx = int(system.width / 2)
		body.real = vec(body.x, body.y)
		body.bounce.y = 0
		system.entities.bodies[entity] = body
		# Override provided controls
		controls = system.entities.players[entity].controls
		if up: controls['up'] = up
		if left: controls['left'] = left
		if down: controls['down'] = down
		if right: controls['right'] = right
		if jump: controls['jump'] = jump

	create_balls(15)
	create_player()
