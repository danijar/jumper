import pygame, time


class Player(object):
	def __init__(self):
		self.speed = 4.0
		self.controls = {
			'up': pygame.K_w,
			'left': pygame.K_a,
			'down': pygame.K_s,
			'right': pygame.K_d,
			'jump': pygame.K_w,
			'attack': pygame.K_SPACE
		}
		self.number = 1
		self.health = 3
		self.ammo = 5
		self.last_attack = time.clock()
