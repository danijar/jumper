import pygame, time


class Animation(object):
	animations = {}

	def __init__(self, path, frames, duration=1.0):
		self.path = path
		self.image = pygame.image.load(self.path)
		self.frames = frames
		self.speed = duration / self.frames
		self.width = self.image.get_width() / frames
		self.height = self.image.get_height()
	
	def cache(self):
		"""Add instance to the global collection"""
		Animation.animations[self.path] = self


class Animated(object):
	def __init__(self):
		self.animation = None
		self.current = 0
		self.repeat = False
		self.switched = None
		self.next = None
		self.running = False

	def play(self, path, repeat=False, restart=True, next=None):
		if path not in Animation.animations:
			raise 'Please create and cache the animation before using it'
		if not restart:
			if self.is_playing(path):
				return
		self.animation = Animation.animations[path]
		self.repeat = repeat
		self.current = 0
		self.switched = time.clock()
		self.next = next
		self.running = True

	def stop(self):
		self.running = False

	def is_playing(self, path=None, endswith=None):
		if not self.running:
			return False
		elif path:
			return self.animation.path == path
		elif endswith:
			return self.animation.path.endswith(endswith)

	def get_frame(self):
		offset = self.current * self.animation.width
		clipping = pygame.Rect(offset, 0, self.animation.width, self.animation.height)
		image = self.animation.image.subsurface(clipping)
		return image
