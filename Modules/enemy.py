import pygame, math
pygame.init()
from pygame.locals import *

from Data.Modules.entity import Entity
from Data.Modules.bullet import Bullet

class Enemy(Entity):
	def __init__(self, loc, width, height, image, reset_value):
		super().__init__(loc, width, height, image)
		
		self.reset_value = reset_value
		self.shoot_timer = self.reset_value
		
		self.shoot_sound = self._load_sound("enemy_shoot", 0.3)
		
	#Private methods
	
	def _shoot(self, bullets, bullets_list):
		self.shoot_timer -= 1
	
		if self.shoot_timer <= 0:
			for bullet in bullets:
				bullets_list.append(bullet)
				
			self._play_sound(self.shoot_sound)
			self.shoot_timer = self.reset_value

	def _get_player_angle(self, player):
		locx, locy = player.loc[0] - self.loc[0], player.loc[1] - self.loc[1]
		angle = math.atan2(locy, locx)

		return angle
		
	def _flip(self, player):
		if player.loc[0] < self.loc[0]:
			self.flip = True
			
		elif player.loc[0] > self.loc[0]:
			self.flip = False