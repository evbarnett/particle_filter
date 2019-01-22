import pygame
from Renderable import *

class Map(Renderable):

	def __init__(self, world_map):
		""" world_map (int[][]): contains 1 for wall, 0 for nothing """
		self.world_map = world_map

	def is_valid(self, x, y):
		if x >= len(self.world_map) or x < 0: return False
		if y >= len(self.world_map[0]) or y < 0: return False
		return self.world_map[x][y] == 0

	def render(self, window, square_width):
		for x in range(len(self.world_map)):
			for y in range(len(self.world_map[0])):
				rect = (x * square_width, y * square_width, (x+1) * square_width, (y+1) * square_width)
				if self.world_map[x][y] == 1:
					pygame.draw.rect(window, (0, 0, 0), rect)
				else:
					pygame.draw.rect(window, (255, 255, 255), rect)