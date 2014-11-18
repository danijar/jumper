import pygame


class Movement(object):
	def __init__(self, direction=[0, 0], speed=1):
		self.direction = direction
		self.speed = speed

class Body(pygame.Rect):
	def __init__(self, rect):
		super().__init__(rect.left, rect.top, rect.width, rect.height)
		self.float_x = float(self.x)
		self.float_y = float(self.y)
	def move(self, way):
		self.float_x += way[0]
		self.float_y += way[1]
		self.x = int(self.float_x)
		self.y = int(self.float_y)
