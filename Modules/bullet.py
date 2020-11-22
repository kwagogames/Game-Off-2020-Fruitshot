import pygame
pygame.init()
from pygame.locals import *

from Data.Modules.entity import Entity

class Bullet(Entity):
	def __init__(self, loc, width, height, vel, dir, image, animation):
		super().__init__(loc, width, height, image)

		self.vel = vel
		self.dir = dir
		

	# Private methods
	def _handle_collisions(self, tiles):
		collided = self._collide(tiles)

		if collided["horizontal"] or collided["vertical"]:
			self._kill()

	#Public methods

	def update(self, tiles):
		self._handle_collisions(tiles)
		self._update_movement()
		self._translate((self.vel[0] * self.dir[0], self.vel[1] * self.dir[1]))
		self._update_current_frame(0.5)
		
	def draw(self, surf, scroll):

		if self.image != None:
			surf.blit(pygame.transform.flip(self.image, self.flip, False), (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
		
