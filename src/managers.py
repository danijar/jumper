import uuid


class Entities(object):
	def __init__(self):
		self.sprites = {}
		self.bodies = {}
		self.movements = {}
		self.players = {}
		self.texts = {}
		self.rails = {}
	def create(self):
		return uuid.uuid4()
	def remove(self, entity):
		self.sprites.pop(entity, None)
		self.bodies.pop(entity, None)
		self.movements.pop(entity, None)
		self.players.pop(entity, None)
		self.texts.pop(entity, None)
		self.rails.pop(entity, None)
