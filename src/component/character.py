import pygame, time


class Character(object):
	def __init__(self):
		self.speed = 4.0
		self.health = 3
		self.ammo = 5
		self.last_attack = time.clock()
