import pygame, time


class Source(object):
	def __init__(self, path, frames):
		self.path = path
		self.image = pygame.image.load(self.path)
		self.frames = frames
		self.width = self.image.get_width() / frames
		self.height = self.image.get_height()


class Animation(object):
	sources = {}

	def __init__(self):
		self.source = None
		self.current = 0
		self.repeat = True
		self.speed = .5
		self.switched = None
		self.running = False
		self.next = None

	def load(path, frames):
		Animation.sources[path] = Source(path, frames)

	def play(self, path, repeat=True, next=None, speed=.5):
		if path not in Animation.sources:
			raise 'Must load animation first'
		self.source = Animation.sources[path]
		self.repeat = repeat
		self.speed = speed
		self.current = 0
		self.switched = time.clock()
		self.running = True
		self.next = next

	def update(self):
		if not self.running:
			return
		if self.switched + self.speed < time.clock():
			self.switched = time.clock()
			if self.current < self.source.frames - 1:
				# Go to next frame
				self.current += 1
			else:
				# Reached end of sprite animation
				if self.repeat:
					self.current = 0
				elif self.next:
					self.play(self.next, repeat=True, next=None)
				else:
					self.running = False

	def get_image(self):
		window = pygame.Rect(self.current * self.source.width, 0, self.source.width, self.source.height)
		image = self.source.image.subsurface(window)
		return image
