import pygame, time
from vec import vec


class Player(object):
	def __init__(self, engine):
		self.engine = engine
		self.engine.events.listen('keydown', self.keydown)

	def keydown(self, key):
		for entity in self.engine.entities.players:
			player = self.engine.entities.players[entity]
			character = self.engine.entities.characters.get(entity)
			body = self.engine.entities.bodies.get(entity)
			# Attack
			if key == player.controls['attack']:
				# Find players in range
				for other_entity in self.engine.entities.players:
					if entity == other_entity:
						continue
					other_player = self.engine.entities.players[other_entity]
					other_body = self.engine.entities.bodies.get(other_entity)
					other_character = self.engine.entities.characters.get(entity)
					# Compute time from last attack and distance to target
					now = time.clock()
					cooldown = now - character.last_attack
					distance = (vec(other_body.center) - vec(body.center)).length()
					# Check if other player near enough and cool down has finished
					if cooldown > 1.5 and distance < 50.0:
						if character.ammo > 0:
							character.last_attack = now
							character.ammo -= 1
							other_character.health -= 1

	def update(self):
		self.update_input()

	def update_input(self):
		"""Handle movement from user input"""
		keys = pygame.key.get_pressed()
		for entity in self.engine.entities.players:
			player = self.engine.entities.players[entity]
			body = self.engine.entities.bodies.get(entity)
			character = self.engine.entities.characters.get(entity)
			if body:
				if keys[player.controls['right']]:
					body.velocity.x = character.speed
				if keys[player.controls['left']]:
					body.velocity.x = -character.speed
				if keys[player.controls['jump']]:
					if body.standing:
						body.velocity.y = -2.5 * character.speed
