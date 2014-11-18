import pygame
from managers import Entities


class System(object):
	def __init__(self):
		self.entities = Entities()
		self.running = True
		self.width = 800
		self.height = 600
