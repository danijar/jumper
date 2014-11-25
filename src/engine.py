import pygame
from managers import Entities, Events


class Engine(object):
	def __init__(self):
		self.entities = Entities()
		self.events = Events()
		self.running = True
		self.width = 640
		self.height = 480
