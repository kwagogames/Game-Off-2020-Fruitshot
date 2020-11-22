import pygame
pygame.init()
from pygame.locals import *

from Data.Modules.enemy import Enemy
from Data.Modules.bullet import Bullet

class Limon(Enemy):
	def __init__(self, loc):
		super().__init__(loc, 64, 56, None, 135)
		
		self._load_animation("Data/Sprites/Enemy_Anims/Limon", "idle", 3)
		self.current_animation = self.animations["idle"]
		
	#Public methods
	def update(self, tiles, player, bullets_list):
		bullet_img = "Data/Sprites/Enemy_Anims/Limon/bullet.png"
		
		bullet_dir = 1
		
		if self.flip:
			bullet_dir = -1
		else:
			bullet_dir = 1
		
		self._flip(player)
		self._shoot([Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [3, 0], [bullet_dir, 0], bullet_img, None),
					Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [4, 3], [bullet_dir, -1], bullet_img, None),
					Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [4, 3], [bullet_dir, 1], bullet_img, None)], bullets_list)
		self._update_current_frame(0.1)