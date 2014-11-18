import sys, pygame, time, random
from properties import Body, Movement
import modules

# Initialize engine
pygame.init()
system = modules.System()
module_window = modules.Window(system)
module_movement = modules.Movement(system)
module_sprite = modules.Sprite(system)

# Create ball
def create_ball():
	entity = system.entities.create()
	system.entities.sprites[entity] = pygame.image.load("asset/texture/circle.png")
	system.entities.bodies[entity] = Body(system.entities.sprites[entity].get_rect())
	system.entities.movements[entity] = Movement([1, 1])
	return entity

for i in range(100):
	entity = create_ball()
	sprite = system.entities.sprites[entity]
	length = int(30 + (20 * random.random()))
	sprite = pygame.transform.scale(sprite, [length, length])
	system.entities.bodies[entity] = Body(sprite.get_rect())
	system.entities.sprites[entity] = sprite
	speed = 1.0 + (4.0 * random.random())
	system.entities.movements[entity].speed = speed

# Main loop
start = 0
while system.running:
	# Measure frame time
	delta = time.clock() - start
	start = time.clock()

	# Update modules
	module_window.update()
	module_movement.update()
	module_sprite.update()

	# Show render buffer on screen
	pygame.display.flip()

	# Sleep until frame ends
	wait = max(0.016 - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
sys.exit()
