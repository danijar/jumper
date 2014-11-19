import pygame
from vec import vec


class Body(pygame.Rect):
	def __init__(self, rect):
		super().__init__(rect.left, rect.top, rect.width, rect.height)
		self.real = vec(self.x, self.y)
		self.velocity = vec()
	def move(self, vector):
		self.real += vector
		self.x = int(self.real.x)
		self.y = int(self.real.y)
	def reinitialize_x(self):
		"""Update float value coordinates from grid position, should
		be used after setting a coordinate with e.g. body.left"""
		self.real.x = float(self.x)
	def reinitialize_y(self):
		self.real.y = float(self.y)

class Player(object):
	def __init__(self):
		self.speed = 3.0
		self.controls = {
			'up': pygame.K_w,
			'left': pygame.K_a,
			'down': pygame.K_s,
			'right': pygame.K_d,
			'jump': pygame.K_SPACE,
		}
