import sys, pygame, time, uuid, random

# Initialize application
pygame.init()
width, height = 800, 600
pygame.display.set_icon(pygame.image.load("asset/other/icon.png"))
pygame.display.set_caption("Window")
pygame.display.set_mode((width, height))
screen = pygame.display.get_surface()

# Movement property
class Movement(object):
	def __init__(self, direction=[0, 0], speed=1):
		self.direction = direction
		self.speed = speed

# Property collections
class Entities(object):
	def __init__(self):
		self.sprites = {}
		self.bodies = {}
		self.movements = {}
	def create(self):
		return uuid.uuid4()
	def remove(self, entity):
		self.sprites.pop(entity, None)
		self.bodies.pop(entity, None)
		self.movements.pop(entity, None)

entities = Entities()

# Create ball
def create_ball():
	entity = entities.create()
	entities.sprites[entity] = pygame.image.load("asset/texture/circle.png")
	entities.bodies[entity] = entities.sprites[entity].get_rect()
	entities.movements[entity] = Movement([1, 1])
	return entity

for i in range(10):
	entity = create_ball()
	entities.movements[entity].speed = (i + 1)

# Main loop
running = True
start = 0
while running:
	# Measure frame time
	delta = time.clock() - start
	start = time.clock()

	# Handle window events
	for event in pygame.event.get():
		# Allow application to quit
		if event.type == pygame.QUIT:
			running = False
		# User pressed a key
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			elif event.key == pygame.K_c and event.mod & pygame.KMOD_LCTRL:
				running = False

	# Update move properties
	for entity in entities.movements:
		movement = entities.movements.get(entity)
		body = entities.bodies.get(entity)
		if body:
			# Move in current direction with current speed
			way = [x * movement.speed for x in movement.direction]
			body = body.move(way)
			# Bounce from window borders
			if body.left < 0 or body.right > width:
				movement.direction[0] *= -1
			if body.top < 0 or body.bottom > height:
				movement.direction[1] *= -1
			# Store result
			entities.movements[entity] = movement
			entities.bodies[entity] = body

	# Render sprites
	screen.fill((0, 0, 0))
	for entity in entities.sprites:
		sprite = entities.sprites.get(entity)
		body = entities.bodies.get(entity)
		if body:
			screen.blit(sprite, body)
	pygame.display.flip()

	# Sleep until frame ends
	wait = max(0.016 - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
sys.exit()
