import pygame
from defs import *
import random

class Barrier():

	def __init__(self, gameDisplay, x, y):
		self.gameDisplay = gameDisplay
		self.state = OBSTACLE_MOVING
		self.img = pygame.image.load(OBSTACLE_FILENAME)
		self.rect = self.img.get_rect()
		self.set_position(x, y)

	def set_position(self, x, y): 
		self.rect.left = x #distance from the left of the screen
		self.rect.top = y #distance from the top of the screen

	def move_position(self, dx, dy):
		self.rect.centerx += dx
		self.rect.centery += dy #forse non mi serve

	def draw(self):
		self.gameDisplay.blit(self.img, self.rect)

	def check_status(self):
		if self.rect.right < 0:
			self.state = OBSTACLE_DONE

	def update(self, dt):
		if self.state == OBSTACLE_MOVING:
			self.move_position(-(OBSTACLE_SPEED * dt), 0) #(dx, dy)
			self.draw()
			self.check_status()

class BarrierCollection():

	def __init__(self, gameDisplay):
		self.gameDisplay = gameDisplay
		self.obstacles = [] #empty vector of obstacles

	def add_new_obstacle(self, x):
		y = 472
		new_obstacle = Barrier(self.gameDisplay, x, y)
		self.obstacles.append(new_obstacle)

	def create_new_set(self):
		self.obstacles = []
		placed = OBSTACLE_FIRST

		while placed < DISPLAY_W:
			self.add_new_obstacle(placed)
			placed += random.randrange(400, 600, 50)

	def update(self, dt):
		rightmost = 0
		for p in self.obstacles:
			p.update(dt)
			if p.rect.left > rightmost:
				rightmost = p.rect.left

		if rightmost < (DISPLAY_W - random.randrange(400, 600, 50)):
			self.add_new_obstacle(DISPLAY_W)

		self.obstacles = [p for p in self.obstacles if p.state == OBSTACLE_MOVING]








