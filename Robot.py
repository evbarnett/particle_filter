from Renderable import *
import random
import math
import pygame

class Robot(Renderable):

	def __init__(self, x, y, angle, vel, rot_vel):
		""" x, y (float): position 
			angle (int): angle in degrees
			weight (float): strength of particle
		"""
		self.x = x
		self.y = y
		self.angle = angle
		self.angle_dir = 1
		self.vel = vel
		self.rot_vel = rot_vel
		self.diameter = 1

	def move(self, wmap):
		start_angle = self.angle
		if random.randint(0, 20) == 0:
			if self.rot_vel == 0:
				self.rot_vel = random.randint(-1, 1)
			self.rot_vel = self.rot_vel * -1
		if random.randint(0, 40) == 0:
			self.rot_vel = 0
		self.angle = self.angle + self.rot_vel * self.rot_vel

		moved_vel = 0
		is_blocked = True

		rad = 3.14 / 180.0 * self.angle
		newx = self.x + math.cos(rad) * self.vel
		newy = self.y + math.sin(rad) * self.vel
		if(wmap.is_valid(int(newx), int(newy)) and 
			wmap.is_valid(int(newx + self.diameter / 2.0), int(newy + self.diameter / 2.0)) and 
			wmap.is_valid(int(newx - self.diameter / 2.0), int(newy - self.diameter / 2.0))):
			self.x = newx
			self.y = newy
			moved_vel = self.vel
			is_blocked = False
		else:
			self.angle = random.randint(0, 359)

		"""The robot turned by +[0] degrees then moved in that direction by moved_vel, and is_blocked is true when moved_vel is 0  because blocked"""
		return (self.angle - start_angle, moved_vel, is_blocked)

	def render(self, window, square_width):
		rad = 3.14 / 180.0 * self.angle
		pygame.draw.circle(window, (100, 100, 100), 
			(int(self.x * square_width), int(self.y * square_width)), int(square_width * self.diameter / 2))
		pygame.draw.line(window, (200, 100, 100), 
			(int(self.x * square_width), int(self.y * square_width)), 
			(int(square_width * (self.x + math.cos(rad) * self.diameter / 2)), int(square_width * (self.y + math.sin(rad) * self.diameter / 2)))) 