import pygame


class Body(pygame.Rect):
	def __init__(self, rect):
		super().__init__(rect.left, rect.top, rect.width, rect.height)
		self.real = [float(self.x), float(self.y)]
		self.velocity = [0.0, 0.0]
	def move(self, way):
		self.real[0] += way[0]
		self.real[1] += way[1]
		self.x = int(self.real[0])
		self.y = int(self.real[1])

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
