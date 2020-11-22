import pygame, random
pygame.init()
from pygame.locals import *

class ParticleSpawner(object):
	def __init__(self, loc, color, gravity, min_spread, max_spread, y_vel, min_life_time, max_life_time, is_infinite, amount):
		self.particles = []

		self.loc = loc
		self.color = color
		self.gravity = gravity
		self.amount = amount
		self.min_spread = min_spread
		self.max_spread = max_spread
		self.y_vel = y_vel
		self.min_life_time = min_life_time
		self.max_life_time = max_life_time
		
		if is_infinite:
			self.is_infinite = True
		else:
			self.is_infinite = False
			
			for i in range(0, self.amount):
				self.particles.append({"loc": [self.loc[0], self.loc[1]], 
				"vel": [random.randint(self.min_spread, self.max_spread) / 10 - 1, self.y_vel], 
				"timer": random.randint(self.min_life_time, self.max_life_time)})

	#Public methods
	def process_particles(self):
		if self.is_infinite:
			self.particles.append({"loc": [self.loc[0], self.loc[1]], 
				"vel": [random.randint(self.min_spread, self.max_spread) / 10 - 1, self.y_vel], 
				"timer": random.randint(self.min_life_time, self.max_life_time)})

		for i, particle in sorted(enumerate(self.particles), reverse = True):
			particle["loc"][0] += particle["vel"][0]
			particle["loc"][1] += particle["vel"][1]
			particle["timer"] -= 0.1
			particle["loc"][1] += self.gravity
			
			if particle["timer"] <= 0:
				self.particles.pop(i)

	def draw_particles(self, surf, scroll):
		for particle in self.particles:
			pygame.draw.circle(surf, self.color, [int(particle["loc"][0] - scroll[0]), int(particle["loc"][1] - scroll[1])], int(particle["timer"]))