#Initialize pygame
import pygame, math
pygame.init()
from pygame.locals import *

from Data.Modules.ball import Ball
from Data.Modules.entity import Entity

#OwO OwO It's the player class
class Player(Entity):
	#Initialize the player class
	def __init__(self, loc):
		super().__init__(loc, 32, 64, None)
		
		self.balls = []
		self.vel = 5
		
		self.hitbox = pygame.Rect((self.loc[0], self.loc[1]), (5, 5))
		
		self.health = 10
		self.hit_timer = 2

		self.left = False
		self.right = False
		self.up = False
		self.down = False
		
		self._load_animation("Data/Sprites/Player_Anims", "walk_back", 3)
		self._load_animation("Data/Sprites/Player_Anims", "walk_front", 3)
		self._load_animation("Data/Sprites/Player_Anims", "walk_side", 2)
		self._load_animation("Data/Sprites/Player_Anims", "idle_back", 1)
		self._load_animation("Data/Sprites/Player_Anims", "idle_front", 1)
		self._load_animation("Data/Sprites/Player_Anims", "idle_side", 1)
		
		self.current_animation = self.animations["idle_side"]
		self.flip_on_movement = True
		
		self.vertically_facing = 0
		
		self.throw_sound = self._load_sound("throw_ball", 0.5)
		self.player_hurt = self._load_sound("player_hurt", 0.5)
		
	#Private methods

	def _shoot(self, scroll):
		self._play_sound(self.throw_sound)	
		
		mx, my = pygame.mouse.get_pos()
	
		sx, sy = self.loc[0] - scroll[0], self.loc[1] - scroll[1]
		
		dx, dy = mx - sx, my - sy
		angle = math.atan2(dy, dx)
							
		self.balls.append(Ball([self.loc[0], self.loc[1]], [math.cos(angle), math.sin(angle)]))

	#Moves the player.
	def _move(self):
		self._update_movement()

		if self.left:
			self._translate((-self.vel, 0))
			self.vertically_facing = 0
		elif self.right:
			self._translate((self.vel, 0))
			self.vertically_facing = 0
			
		if self.up:
			self._translate((0, -self.vel))
			self.vertically_facing = -1
		elif self.down:
			self._translate((0, self.vel))
			self.vertically_facing = 1
			
	def _set_hitbox(self, bullets):
		self.hitbox = pygame.Rect((self.loc[0] + 11, self.loc[1] + 32), (5, 5))
		
		for ball in self.balls:
			if ball.rect.colliderect(self.hitbox):
				if ball.harmful:
					if self.hit_timer == 2:
						self.health -= 4
						self.hit_timer = -30
						self._play_sound(self.player_hurt)
						
		for bullet in bullets:
			if bullet.rect.colliderect(self.hitbox):
				if self.hit_timer == 2:
					bullet._kill()
					self.health -= 1
					self.hit_timer = -30
					self._play_sound(self.player_hurt)
						
	def _set_hit_timer(self):
		if self.hit_timer < 2:
			self.hit_timer += 1
			
	#Manage the balls that the player has thrown.
	def _update_balls(self, tiles, enemies):
		if not self.gone:
			for ball in self.balls:
				if not ball.gone:
					ball.update(tiles, enemies, self)
				else:
					self.balls.remove(ball)

	def _animate(self):
		if self.movement != [0, 0]:
			if self.vertically_facing == -1:
				self._change_animation(self.animations["walk_back"])
			elif self.vertically_facing == 1:
				self._change_animation(self.animations["walk_front"])
			elif self.vertically_facing == 0:
				self._change_animation(self.animations["walk_side"])
		else:
			if self.vertically_facing == -1:
				self._change_animation(self.animations["idle_back"])
			elif self.vertically_facing == 1:
				self._change_animation(self.animations["idle_front"])
			elif self.vertically_facing == 0:
				self._change_animation(self.animations["idle_side"])
				
	def _check_health(self):
		if self.health <= 0:
			self.gone = True


	#Public methods

	#Get input from the player!
	def get_input(self, event, scroll):
		if event.type == KEYDOWN:
			if event.key == K_a:
				self.left = True
			elif event.key == K_d:
				self.right = True

			
			if event.key == K_w:
				self.up = True
			elif event.key == K_s:
				self.down = True

		if event.type == KEYUP:
			if event.key == K_a:
				self.left = False
			elif event.key == K_d:
				self.right = False
			
			if event.key == K_w:
				self.up = False
			elif event.key == K_s:
				self.down = False
				
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				self._shoot(scroll)
				
	#Draws the player.
	def draw(self, surf, scroll):
		if not self.gone:
			if self.image != None:
				surf.blit(pygame.transform.flip(self.image, self.flip, False), (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))
						
			for ball in self.balls:
				ball.draw(surf, scroll)


	#This just updates the player.
	def update(self, tiles, enemies, bullets):
		self._move()
		self._collide(tiles)
		self._set_hitbox(bullets)
		self._set_hit_timer()
		self._check_health()
		self._update_balls(tiles, enemies)
		self._update_current_frame(0.1)
		self._animate()