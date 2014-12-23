import pygame, time, copy
from vec import vec


class Character(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		"""Update all sub systems"""
		self.update_healths()
		self.update_hits()
		self.update_attacks()

	def update_healths(self):
		"""Remove dead characters"""
		for entity, character in self.engine.entities.characters.copy().items():
			if character.health < 1:
				animated = self.engine.entities.animations.get(entity)
				if animated and animated.is_playing('hit'):
					# Add callback to animation that removes the entity
					current_entity = copy.deepcopy(entity)
					remove = lambda: self.remove_character(current_entity)
					animated.play('hit', restart=False, next=remove)
				else:
					self.remove_character(entity)

	def update_hits(self):
		"""Hit enemies when objects fall on them"""
		for entity, character in self.engine.entities.characters.copy().items():
			animated = self.engine.entities.animations.get(entity)
			# Skip players to allow them move objects on their head
			if entity in self.engine.entities.players:
				continue
			# Fetch components
			body = self.engine.entities.bodies.get(entity)
			if not body:
				continue
			# Hit enemy for each object on top
			for other in body.ontops.copy():
				if character.hit():
					other.bounce_from(body)
					if animated:
						animated.play('hit', restart=False)

	def update_attacks(self):
		"""Attack players when they walk into enemies"""
		for enemy in self.engine.entities.characters.copy():
			# Skip players to allow them move objects on their head
			if enemy in self.engine.entities.players:
				continue
			# Fetch components
			enemy_body = self.engine.entities.bodies.get(enemy)
			enemy_character = self.engine.entities.characters.get(enemy)
			if not enemy_body or not enemy_character:
				continue
			# Let enemies attack players they walk into
			for player in self.engine.entities.players:
				player_body = self.engine.entities.bodies.get(player)
				player_character = self.engine.entities.characters.get(player)
				player_animation = self.engine.entities.animations.get(player)
				if not player_body or not player_character:
					continue
				# Check if overlapping with player upper part of body,
				# touching only with feet is allowed for jumping onto them
				if player_body.collide_upper(enemy_body):
					if enemy_character.attack(player_character):
						player_body.bounce_from(enemy_body)
						if player_animation:
							player_animation.play('hit')

	def remove_character(self, entity):
		"""Detach from physics simulation and remove entity"""
		self.engine.entities.bodies[entity].detach()
		self.engine.entities.remove(entity)
