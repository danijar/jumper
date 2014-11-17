import sys, pygame, time

# Initialize application
pygame.init()
width, height = 320, 240
pygame.display.set_icon(pygame.image.load("asset/other/icon.png"))
pygame.display.set_caption("Window")
pygame.display.set_mode((width, height))
screen = pygame.display.get_surface()

# Create ball
sprite = pygame.image.load("asset/texture/circle.png")
body = sprite.get_rect()
direction = [1, 1]
speed = 2

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

	# Move ball and let it bounce from window borders
	body = body.move([x * speed for x in direction])
	if body.left < 0 or body.right > width:
		direction[0] = -direction[0]
	if body.top < 0 or body.bottom > height:
		direction[1] = -direction[1]

	# Render sprite
	screen.fill((0, 0, 0))
	screen.blit(sprite, body)
	pygame.display.flip()

	# Sleep until frame ends
	wait = max(0.016 - delta, 0)
	time.sleep(wait)

# Cleanup resources
pygame.quit()
sys.exit()
