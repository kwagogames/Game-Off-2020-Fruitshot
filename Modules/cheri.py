import pygame
pygame.init()
from pygame.locals import *

from Data.Modules.enemy import Enemy
from Data.Modules.bullet import Bullet


class Cheri(Enemy):
	def __init__(self, loc):
		super().__init__(loc, 63, 64, None, 120)

		self._load_animation("Data/Sprites/Enemy_Anims/Cheri", "idle", 8)
		self.current_animation = self.animations["idle"]

	#Public methods
	def update(self, tiles, player, bullets_list):
		bullet_img = "Data/Sprites/Enemy_Anims/Cheri/bullet.png"
		
		self._flip(player)
		self._shoot([Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [0, 3], [0, 1], bullet_img, None),
					 Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [3, 3], [-1, 1], bullet_img, None),
					 Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [3, 3], [1, 1], bullet_img, None)], bullets_list)
		self._update_current_frame(0.1)
