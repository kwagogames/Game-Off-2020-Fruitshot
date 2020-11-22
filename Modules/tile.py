import pygame
pygame.init()
from pygame.locals import *

from Data.Modules.entity import Entity

class Tile(Entity):
	def __init__(self, loc, image, tile_size, quad):
		super().__init__(loc, tile_size, tile_size, image)
		
		self.tile_size = tile_size
		self.quad = quad		
		
	#Public methods
	def draw(self, surf, scroll):
		surf.blit(self.image, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]), (0, self.quad * self.tile_size, self.tile_size, self.tile_size))