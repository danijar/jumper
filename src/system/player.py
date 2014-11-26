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
					# Check if other player near enough and cool down has finished
					now = time.clock()
					if character.last_attack and now - character.last_attack < character.attack_time:
						continue
					if (vec(other_body.center) - vec(body.center)).length() > character.attack_range:
						continue
					# Perform attack
					character.last_attack = now
					other_character.health -= 1

	def update(self):
		self.input()
		
	def input(self):
		"""Handle movement from user input"""
		keys = pygame.key.get_pressed()
		for entity in self.engine.entities.players:
			player = self.engine.entities.players[entity]
			body = self.engine.entities.bodies.get(entity)
			character = self.engine.entities.characters.get(entity)
			# Freeze player for a while after being hit
			if character.last_hit and time.clock() - character.last_hit < character.hit_time:
				continue
			# Move body by user input
			if body:
				if keys[player.controls['right']]:
					body.velocity.x = character.speed
				if keys[player.controls['left']]:
					body.velocity.x = -character.speed
				if keys[player.controls['jump']]:
					if body.standing:
						body.velocity.y = -2.5 * character.speed

