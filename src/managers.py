import uuid

class Entities(object):
	def __init__(self):
		self.sprites = {}
		self.bodies = {}
		self.movements = {}
	def create(self):
		return uuid.uuid4()
	def remove(self, entity):
		self.sprites.pop(entity, None)
		self.bodies.pop(entity, None)
		self.movements.pop(entity, None)