import pygame


class Player(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		self.update_input()

	def update_input(self):
		"""Handle movement from user input"""
		keys = pygame.key.get_pressed()
		for entity in self.engine.entities.players:
			player = self.engine.entities.players[entity]
			body = self.engine.entities.bodies[entity]
			if body:
				if keys[player.controls['right']]:
					body.velocity.x = player.speed
				if keys[player.controls['left']]:
					body.velocity.x = -player.speed
				if keys[player.controls['jump']]:
					if body.standing:
						body.velocity.y = -2.5 * player.speed
