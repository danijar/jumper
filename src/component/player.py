import pygame


class Player(object):
	def __init__(self):
		self.speed = 4.0
		self.controls = {
			'up': pygame.K_w,
			'left': pygame.K_a,
			'down': pygame.K_s,
			'right': pygame.K_d,
			'jump': pygame.K_SPACE,
		}
		self.health = 5
		self.ammo = 5
