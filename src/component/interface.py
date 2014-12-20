import pygame


class Interface(object):
	def evaluate(self):
		pass


class InterfaceText(Interface):
	def __init__(self, message=lambda: ''):
		"""Evaluate return the text to display"""
		self.message = message

	def evaluate(self):
		message = self.message()
		font = pygame.font.Font('asset/font/source.ttf', 16)
		sprite = font.render(message, True, (255, 255, 255))
		return sprite


class InterfaceHealth(Interface):
	heart = pygame.image.load('asset/texture/heart.png')
	heart = pygame.transform.scale(heart, [20, 20])

	def __init__(self, character, top=None, bottom=None, left=None, right=None):
		self.character = character
		self.top = top
		self.bottom = bottom
		self.left = left
		self.right = right

	def evaluate(self):
		health = 1# self.character.health if self.character else 0
		rect = InterfaceHealth.heart.get_rect()
		sprite = pygame.Surface((rect.w * health, rect.h), flags=pygame.SRCALPHA)
		sprite.fill((0, 0, 0, 0))
		for i in range(health):
			rect.left = i * rect.w
			sprite.blit(InterfaceHealth.heart, rect)
		position = sprite.get_rect()
		if self.left:
			position.left = self.left
		elif self.right:
			position.right = self.right
		if self.top:
			position.top = self.top
		elif self.bottom:
			position.bottom = self.bottom
		return sprite, position
