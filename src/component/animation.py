import pygame, time


class Animation(object):
	def __init__(self, path, frames, duration=1.0):
		self.path = path
		self.image = pygame.image.load(self.path)
		self.frames = frames
		self.speed = duration / self.frames
		self.width = self.image.get_width() / frames
		self.height = self.image.get_height()


class Animated(object):
	def __init__(self, animations):
		"""Pass a dict from names to Animation objects that this component is
		capable of"""
		self.animations = animations
		self.current_name = None
		self.current_animation = None
		self.current_frame = 0
		self.repeat = False
		self.switched = None
		self.next = None
		self.running = False

	def play(self, name, repeat=False, restart=True, next=None):
		if name not in self.animations:
			raise 'The component does not know this animation'
		self.repeat = repeat
		self.next = next
		if not restart:
			if self.is_playing(name):
				return
		self.current_name = name
		self.current_animation = self.animations[name]
		self.current_frame = 0
		self.switched = time.clock()
		self.running = True

	def stop(self):
		self.running = False

	def is_playing(self, name=None):
		if self.running and name:
			return self.current_name == name
		return False

	def get_frame(self):
		offset = self.current_frame * self.current_animation.width
		clipping = pygame.Rect(offset, 0, self.current_animation.width, self.current_animation.height)
		image = self.current_animation.image.subsurface(clipping)
		return image
