import pygame, time
from engine import Engine
from system.window import Window
from system.player import Player
from system.body import Body
from system.text import Text
from system.sprite import Sprite
from system.level import Level

# Initialize engine
pygame.init()
engine  = Engine()
windows = Window(engine)
players = Player(engine)
bodys   = Body(engine)
texts   = Text(engine)
sprites = Sprite(engine)
level   = Level(engine)

# Create label to display frame time
text = engine.entities.create()

# Main loop
start = 0
while engine.running:
	# Measure frame time
	start = time.clock()

	# Update systems
	windows.update()
	players.update()
	bodys.update()
	texts.update()
	sprites.update()
	level.update()

	# Show render buffer on screen
	pygame.display.flip()

	# Sleep until frame ends
	delta = time.clock() - start
	engine.entities.texts[text] = 'Frametime: ' + str(round(delta * 1000, 1)) + 'ms'
	wait = max((1 / 60) - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
