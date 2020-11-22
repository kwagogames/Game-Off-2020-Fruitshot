import pygame, random
pygame.init()
from pygame.locals import *

from Data.Modules.entity import Entity
from Data.Modules.particle_spawner import ParticleSpawner

#The ball class. This is the player's main (and only) form of attack
class Ball(Entity):
	def __init__(self, loc, dir):
		super().__init__(loc, 32, 32, "Data/Sprites/Player_Anims/ball.png")
		
		self.harmful_image = pygame.image.load("Data/Sprites/Player_Anims/ball_harmful.png").convert()
		self.harmful_image.set_colorkey((0, 0, 0))
		
		self.dir = dir 
		self.vel = 6
		
		self.bounce_counts = 0
		self.harmful = False
		self.gone = False
		
		self.bounce_sound = self._load_sound("ball_bounce", 0.5)
	
	#Private methods

	#Handles collisions.
	def _handle_collisions(self, tiles, enemies, player):
		collided = self._collide(tiles)
		

		if collided["vertical"]:
			self.dir[1] *= -1
			self._play_sound(self.bounce_sound)
			
		if collided["horizontal"]:
			self.dir[0] *= -1
			self._play_sound(self.bounce_sound)
			
		if collided["vertical"] or collided["horizontal"]:
			if not self.harmful:
				self.harmful = True
				self.vel = 8
				self._play_sound(self.bounce_sound)
			
			self.bounce_counts += 1
			
		for enemy in enemies:
			if self.rect.colliderect(enemy.rect):
				enemy._kill()
				
				if not self.harmful:
					self.harmful = True
					self.vel = 8
				
				self.bounce_counts += 1
				self.dir[1] *= -1
				self.dir[0] *= -1
				self._play_sound(self.bounce_sound)
				
		if self.rect.colliderect(player.hitbox):
			if self.harmful:
				if not player.gone:
					self.bounce_counts += 1
					self.dir[1] *= -1
					self.dir[0] *= -1
					self._play_sound(self.bounce_sound)
			
	def _count_bounce_counts(self):
		if self.bounce_counts > 2:
			self._kill()
			
	def _set_image(self):
		if self.harmful:
			self.image = self.harmful_image

	#Move!
	def _move(self):
		self._update_movement()
		self._translate((self.vel * self.dir[0], self.vel * self.dir[1]))

	#Public methods
	
	def update(self, tiles, enemies, player):
		self._move()
		self._handle_collisions(tiles, enemies, player)
		self._count_bounce_counts()
		self._set_image()
