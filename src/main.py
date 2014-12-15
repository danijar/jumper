import pygame, time
from engine import Engine
from system.window import Window
from system.character import Character
from system.player import Player
from system.movement import Movement
from system.body import Body
from system.text import Text
from system.animation import Animation
from system.sprite import Sprite
from system.level import Level
from component.text import Text as TextComponent


# Initialize engine
pygame.init()
engine     = Engine()
windows    = Window(engine)
characters = Character(engine)
players    = Player(engine)
movements  = Movement(engine)
bodies     = Body(engine)
texts      = Text(engine)
animation  = Animation(engine)
sprites    = Sprite(engine)
level      = Level(engine)

# Create label to display frame time
delta = 0.0
evaluate = lambda: 'Frametime: ' + str(round(delta * 1000, 1)) + 'ms'
engine.entities.texts[engine.entities.create()] = TextComponent(evaluate)

# Main loop
start = 0
while engine.running:
	# Measure frame time
	start = time.clock()

	# Update systems
	windows.update()
	characters.update()
	players.update()
	movements.update()
	bodies.update()
	animation.update()
	sprites.update()
	texts.update()
	level.update()

	# Show render buffer on screen
	pygame.display.flip()

	# Sleep until frame ends
	delta = time.clock() - start
	wait = max((1 / 60) - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
