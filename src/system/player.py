import pygame, time
from vec import vec


class Player(object):
	def __init__(self, engine):
		self.engine = engine
		self.engine.events.listen('keydown', self.keydown)

	def update(self):
		"""Update all sub systems"""
		self.update_second_jumps()
		self.update_inputs()

	def update_second_jumps(self):
		for entity, player in self.engine.entities.players.items():
			body = self.engine.entities.bodies.get(entity)
			if body and body.standing:
				player.second_jump = True
		
	def update_inputs(self):
		"""Handle movement from user input"""
		keys = pygame.key.get_pressed()
		for entity, player in self.engine.entities.players.items():
			# Fetch components
			body = self.engine.entities.bodies.get(entity)
			character = self.engine.entities.characters.get(entity)
			animated = self.engine.entities.animations.get(entity)
			if not body or not character:
				continue
			# Prevent player from being hit right again by disabling user
			# input for a moment
			if character.freezed():
				continue
			# Move body by user input
			left, right = False, False
			if keys[player.controls['right']]:
				body.velocity.x = character.speed
				right = True
			if keys[player.controls['left']]:
				body.velocity.x = -character.speed
				left = True
			# Update animations
			if animated:
				if left:
					animated.play('left', restart=False, repeat=True)
				elif right:
					animated.play('right', restart=False, repeat=True)
				elif body.standing:
					animated.stop()

	def keydown(self, key):
		"""Event handler for key down events"""
		for entity, player in self.engine.entities.players.items():
			# Get properties
			body = self.engine.entities.bodies.get(entity)
			character = self.engine.entities.characters.get(entity)
			# Handle keys
			if key == player.controls['jump'] and body and character:
				if body.standing:
					body.velocity.y = -2.5 * character.speed
				elif player.second_jump:
					player.second_jump = False
					body.velocity.y = -1.8 * character.speed
			if key == player.controls['attack']:
				self.attack(entity)

	def attack(self, entity):
		"""Try to attack other players in range"""
		# Fetch components		
		body = self.engine.entities.bodies.get(entity)
		character = self.engine.entities.characters.get(entity)
		if not body or not character:
			return
		# Find players in range
		for other_entity in self.engine.entities.players:
			if entity == other_entity:
				continue
			# Fetch components
			other_body = self.engine.entities.bodies.get(other_entity)
			other_character = self.engine.entities.characters.get(other_entity)
			other_animation = self.engine.entities.animations.get(other_entity)
			if not other_body or not other_character:
				continue
			# Check if other player near enough
			if (vec(other_body) - vec(body)).length() > character.attack_range:
				continue
			# Try to attack, succeeds if cool down has finished
			if character.attack(other_character):
				other_body.bounce_from(body)
				if other_animation:
					other_animation.play('hit')