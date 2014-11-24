import pygame
from managers import Entities


class Engine(object):
	def __init__(self):
		self.entities = Entities()
		self.running = True
		self.width = 640
		self.height = 480
