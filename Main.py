import pygame
from pygame.locals import *
import random
from Particle import *
from Robot import *
from Renderable import *
from Map import *
import time

world_map = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def main():
	SQUARE_WIDTH = 30
	PARTICLE_MAX = 1000
	print(gen_random_pos(world_map))
	print(gen_random_particle(world_map))
	pygame.init()
	windowSurface = pygame.display.set_mode((len(world_map) * SQUARE_WIDTH, len(world_map[0]) * SQUARE_WIDTH))
	pygame.display.set_caption('Robot Position Estimation w/ a Particle Filter')

	world = Map(world_map)

	pos = gen_robot_start_pos(world_map)
	robot = Robot(pos[0], pos[1], gen_random_angle(), 0.4, 1)

	particles = []

	for i in range(0, PARTICLE_MAX):
		particles.append(gen_random_particle(world_map))

	while True:
		# Main loop
		world.render(windowSurface, SQUARE_WIDTH)
		robot.render(windowSurface, SQUARE_WIDTH)
		tup_move = robot.move(world)

		particles = [p for p in particles if p.weight >= 0.0]

		for p in particles:
			p.handle_move(tup_move, world)
			p.render(windowSurface, SQUARE_WIDTH)

		# resample

		if len(particles) < PARTICLE_MAX / 2:

			total_angle = 0
			total_x = 0
			total_y = 0
			tlen = 0
			for p in particles:
				if p.weight > 1:
					factor = p.weight * p.weight
					total_angle += p.angle * factor
					total_x += p.x * factor
					total_y += p.y * factor
					tlen += factor

			for i in range(0, PARTICLE_MAX - len(particles)):
				if random.randint(0, 6) == 0:
					np = Particle(total_x / tlen + random.uniform(-0.5, 0.5), 
						total_y / tlen + random.uniform(-0.5, 0.5), total_angle / tlen + random.randint(-5, 5), 1.0)
				else:
					np = gen_random_particle(world_map)
				particles.append(np)

			time.sleep(0.05)

		# Events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		# update
		pygame.display.update()


def gen_random_angle():
	return random.randint(0, 359)

def gen_random_particle(world):
	pos = gen_random_pos(world)
	return Particle(pos[0], pos[1], gen_random_angle(), 1.0)

def gen_robot_start_pos(world):
	while True:
		pos = (random.randint(1, len(world) - 1), random.randint(1, len(world[0]) - 1))
		if world[pos[0] - 1][pos[1] - 1] == 0:
			return (pos[0] - 0.5, pos[1] - 0.5)

def gen_random_pos(world):
	return (random.uniform(0, len(world) - 1), random.uniform(0, len(world[0]) - 1))

if __name__ == '__main__':
	main()