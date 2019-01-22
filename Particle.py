from Renderable import *
import pygame
import math

class Particle(Renderable):

	def __init__(self, x, y, angle, weight):
		""" x, y (float): position 
			angle (int): angle in degrees
			weight (float): strength of particle
		"""
		self.x = x
		self.y = y
		self.angle = angle
		self.weight = weight

	def handle_move(self, move_tup, wmap):
		self.angle = self.angle + move_tup[0]
		rad = 3.14 / 180.0 * self.angle
		newx = self.x + math.cos(rad) * move_tup[1]
		newy = self.y + math.sin(rad) * move_tup[1]
		if wmap.is_valid(int(newx), int(newy)):
			if move_tup[2] == True:
				self.weight = self.weight - 0.01
			else:
				self.x = newx
				self.y = newy
				self.weight = self.weight + 0.05
		else:
			self.weight = self.weight - 0.2
			if self.weight > 2: self.weight *= 0.5

	def render(self, window, square_width):
		if self.weight * 10 > 255:
			c = 255
		else:
			c = abs(self.weight * 10)
		pygame.draw.circle(window, (c, 50, 50), 
			(int(self.x * square_width), int(self.y * square_width)), 2)