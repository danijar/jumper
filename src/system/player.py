import pygame, time
from vec import vec


class Player(object):
	def __init__(self, engine):
		self.engine = engine
		self.engine.events.listen('keydown', self.keydown)

	def keydown(self, key):
		for entity in self.engine.entities.players:
			player = self.engine.entities.players[entity]
			body = self.engine.entities.bodies.get(entity)
			# Attack
			if key == player.controls['attack']:
				# Find players in range
				for other_entity in self.engine.entities.players:
					if entity == other_entity:
						continue
					other_player = self.engine.entities.players[other_entity]
					other_body = self.engine.entities.bodies[other_entity]
					# Compute time from last attack and distance to target
					now = time.clock()
					cooldown = now - player.last_attack
					distance = (vec(other_body.center) - vec(body.center)).length()
					# Check if other player near enough and cool down has finished
					if cooldown > 1.5 and distance < 50.0:
						if player.ammo > 0:
							player.last_attack = now
							player.ammo -= 1
							other_player.health -= 1

	def update(self):
		self.update_input()
		self.update_health()

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

	def update_health(self):
		for entity in self.engine.entities.players.copy():
			player = self.engine.entities.players[entity]
			if player.health < 1:
				self.engine.entities.remove(entity)
