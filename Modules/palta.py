import pygame, math
pygame.init()
from pygame.locals import *

from Data.Modules.enemy import Enemy
from Data.Modules.bullet import Bullet

class Palta(Enemy):
	def __init__(self, loc):
		super().__init__(loc, 48, 64, None, 120)

		self._load_animation("Data/Sprites/Enemy_Anims/Palta", "idle", 3)
		self.current_animation = self.animations["idle"]
	
	def update(self, tiles, player, bullets_list):
		bullet_img = "Data/Sprites/Enemy_Anims/Palta/bullet.png"
		
		player_angle = self._get_player_angle(player)
		
		self._flip(player)
		self._shoot([Bullet([self.rect.center[0], self.rect.center[1]], 32, 32, [2, 2], [math.cos(player_angle), math.sin(player_angle)], bullet_img, None)],
		bullets_list)
		self._update_current_frame(0.1)