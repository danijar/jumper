import pygame, time

from component.animation import Animation as Animation_


class Animation(object):
	def __init__(self, engine):
		self.engine = engine

	def update(self):
		# Update sprites of animated entities
		for entity, animated in self.engine.entities.animations.copy().items():
			if entity in self.engine.entities.sprites:
				if not animated.running:
					continue
				if animated.switched + animated.current_animation.speed < time.clock():
					animated.switched = time.clock()
					if animated.current_frame < animated.current_animation.frames - 1:
						# Go to next frame
						animated.current_frame += 1
					else:
						# Reached end of sprite animation
						self.finish(animated)

	def finish(self, animated):
		if animated.repeat:
			animated.current_frame = 0
		else:
			animated.running = False
			if animated.next:
				animated.next()
