import sys, pygame, time, random
from properties import Body, Movement, Player
import modules

# Initialize engine
pygame.init()
system = modules.System()
module_window = modules.Window(system)
module_player = modules.Player(system)
module_movement = modules.Movement(system)
module_sprite = modules.Sprite(system)

# Create balls
def create_ball():
	entity = system.entities.create()
	system.entities.sprites[entity] = pygame.image.load("asset/texture/circle.png")
	system.entities.bodies[entity] = Body(system.entities.sprites[entity].get_rect())
	system.entities.movements[entity] = Movement([1, 1])
	return entity

def create_balls(amount=32):
	for i in range(amount):
		entity = create_ball()
		sprite = system.entities.sprites[entity]
		length = int(30 + (20 * random.random()))
		sprite = pygame.transform.scale(sprite, [length, length])
		system.entities.sprites[entity] = sprite
		system.entities.bodies[entity] = Body(sprite.get_rect())
		speed = 1.0 + (4.0 * random.random())
		system.entities.movements[entity].speed = speed

create_balls(5)

# Create player
def create_player(up=pygame.K_w, left=pygame.K_a, down=pygame.K_s, right=pygame.K_d):
	entity = system.entities.create()
	system.entities.sprites[entity] = pygame.image.load("asset/texture/player.png")
	system.entities.bodies[entity] = Body(system.entities.sprites[entity].get_rect())
	system.entities.movements[entity] = Movement([0, 0], 3)
	system.entities.players[entity] = Player()
	system.entities.players[entity].controls = {
		'up': up,
		'left': left,
		'down': down,
		'right': right
	}

create_player()

# Main loop
start = 0
while system.running:
	# Measure frame time
	delta = time.clock() - start
	start = time.clock()

	# Update modules
	module_window.update()
	module_player.update()
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
