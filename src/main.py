import pygame, time
import system, modules
from initialize import initialize

# Initialize engine
pygame.init()
system = system.System()
module_window = modules.Window(system)
module_player = modules.Player(system)
module_body = modules.Body(system)
module_text = modules.Text(system)
module_sprite = modules.Sprite(system)

# Add balls and player
initialize(system)

# Create text to display frame time
text = system.entities.create()

# Main loop
start = 0
while system.running:
	# Measure frame time
	start = time.clock()

	# Update modules
	module_window.update()
	module_player.update()
	module_body.update()
	module_text.update()
	module_sprite.update()

	# Show render buffer on screen
	pygame.display.flip()

	# Sleep until frame ends
	delta = time.clock() - start
	system.entities.texts[text] = 'Frametime: ' + str(round(delta * 1000, 1)) + 'ms'
	wait = max((1 / 60) - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
