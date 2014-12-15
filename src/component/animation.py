import pygame, time


class Animation(object):
	def __init__(self):
		self.source = None
		self.width = 0
		self.frames = 0
		self.current = 0
		self.speed = .5
		self.repeat = True
		self.running = False

	def load(self, path, frames):
		self.frames = frames
		self.source = pygame.image.load(path)
		self.width = self.source.get_width() / self.frames
		self.running = False

	def update(self):
		if not self.running:
			return
		if self.switched + self.speed < time.clock():
			self.switched = time.clock()
			if self.current < self.frames - 1:
				# Go to next frame
				self.current += 1
			else:
				# Reached end of sprite animation
				if self.repeat:
					self.current = 0
				else:
					self.running = False

	def play(self, repeat=True, speed=.5):
		self.repeat = repeat
		self.speed = speed
		self.current = 0
		self.switched = time.clock()
		self.running = True

	def get_image(self):
		window = pygame.Rect(self.current * self.width, 0, self.width, self.source.get_height())
		image = self.source.subsurface(window)
		return image
