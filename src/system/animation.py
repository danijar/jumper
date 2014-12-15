import pygame, time

from component.animation import Animation as Animation_


class Animation(object):
	def __init__(self, engine):
		self.engine = engine
		# Load animations
		Animation_('asset/animation/player-right.png', 4, 0.5).cache()
		Animation_('asset/animation/player-left.png',  4, 0.5).cache()
		Animation_('asset/animation/player-hit.png',   3, 1.0).cache()
		Animation_('asset/animation/enemy-right.png',  4, 0.5).cache()
		Animation_('asset/animation/enemy-left.png',   4, 0.5).cache()
		Animation_('asset/animation/enemy-hit.png',    3, 1.0).cache()

	def update(self):
		# Update sprites of animated entities
		for entity, animated in self.engine.entities.animations.items():
			if entity in self.engine.entities.sprites:
				if not animated.running:
					continue
				if animated.switched + animated.animation.speed < time.clock():
					animated.switched = time.clock()
					if animated.current < animated.animation.frames - 1:
						# Go to next frame
						animated.current += 1
					else:
						# Reached end of sprite animation
						self.finish(animated)

	def finish(self, animated):
		if animated.repeat:
			animated.current = 0
		else:
			animated.running = False
			if animated.next:
				animated.next()
