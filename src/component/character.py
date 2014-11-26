import pygame, time


class Character(object):
	def __init__(self):
		# Properties
		self.speed = 4.0
		self.attack_time = 1.5
		self.attack_ramge = 55.0
		self.hit_time = 1.5
		# Variables
		self.health = 3
		self.last_attack = None
		self.last_hit = None
