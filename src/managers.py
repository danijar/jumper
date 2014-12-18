import uuid


class Entities(object):
	def __init__(self):
		self.sprites = {}
		self.bodies = {}
		self.movements = {}
		self.characters = {}
		self.players = {}
		self.interfaces = {}
		self.rails = {}
		self.animations = {}

	def create(self):
		return uuid.uuid4()

	def remove(self, entity):
		self.sprites.pop(entity, None)
		self.bodies.pop(entity, None)
		self.movements.pop(entity, None)
		self.characters.pop(entity, None)
		self.players.pop(entity, None)
		self.interfaces.pop(entity, None)
		self.rails.pop(entity, None)
		self.animations.pop(entity, None)


class Events(object):
	def __init__(self):
		self.listeners = {}

	def listen(self, event, callback):
		if event not in self.listeners:
			self.listeners[event] = []
		self.listeners[event].append(callback)

	def fire(self, event, *args, **kwargs):
		if event in self.listeners:
			for callabck in self.listeners[event]:
				callabck(*args, **kwargs)
