import pygame, time


class Character(object):
	def __init__(self):
		self.speed = 3.0
		self.health = 3
		self.attack_time = 1.0
		self.attack_range = 55.0
		self.last_attack = None
		self.hit_time = 1.0
		self.last_hit = None

	def attack(self, target, amount=1):
		"""Attack another character taking attack cooldown and hit protection
		into account"""
		now = time.clock()
		# Character can only attack after attack cooldown finished
		if self.last_attack and now - self.last_attack < self.attack_time:
			return False
		# Try to hit the target character
		if target.hit():
			self.last_attack = now
			return True
		else:
			return False

	def hit(self, amount=1):
		"""Reduce health and set timer to protect for being hit right again"""
		# Don't hit if already been hit within time threshold
		if self.freezed():
			return False
		# Reduce health and update timestamp
		self.last_hit = time.clock()
		self.health -= amount
		return True		

	def freezed(self):
		"""Whether the character currently is protected because of being hit. 
		This is also useful for ignoring user input to prevent walking into
		the enemy right again."""
		return self.last_hit and time.clock() - self.last_hit < self.hit_time
