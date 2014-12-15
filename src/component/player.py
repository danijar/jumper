import pygame, time


class Player(object):
	def __init__(self):
		self.number = 1
		self.controls = {
			'up':     pygame.K_w,
			'left':   pygame.K_a,
			'down':   pygame.K_s,
			'right':  pygame.K_d,
			'jump':   pygame.K_w,
			'attack': pygame.K_SPACE
		}
		self.second_jump = True