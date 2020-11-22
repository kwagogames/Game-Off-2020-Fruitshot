import pygame
pygame.init()
from pygame.locals import *


class Entity(object):
	def __init__(self, loc, width, height, image):
		if image != None:
			self.image = pygame.image.load(image).convert()
			self.image.set_colorkey((0, 0, 0))
		else:
			self.image = None
		
		self.animations = {}
		self.current_animation = None
		self.current_frame = 0
		self.flip_on_movement = False
		self.flip = False
		
		self.loc = loc
		self.width = width
		self.height = height
		self.rect = pygame.Rect((self.loc[0], self.loc[1]), (self.width, self.height))

		self.movement = [0, 0]
		
		self.gone = False
		

	#Private methods
	def _load_animation(self, path, name, frames):
		current_frame = 0
		images = []
		
		while current_frame <= frames - 1:
			image = pygame.image.load(path + "/" + name + "/" + str(current_frame) + ".png").convert()
			image.set_colorkey((0, 0, 0))
			images.append(image)
			
			current_frame += 1
			
		self.animations[name] = images
		
	def _load_sound(self, name, volume):
		sound = pygame.mixer.Sound("Data/Sounds/" + name + ".wav")
		pygame.mixer.Sound.set_volume(sound, volume)
		
		return sound
		
	def _play_sound(self, sound):
		pygame.mixer.Sound.play(sound)
		
	def _change_animation(self, new_anim):
		if self.current_animation != new_anim:
			self.current_animation = new_anim
			self.current_frame = 0
			
	def _update_current_frame(self, fps):
		if self.current_animation != None:
			self.current_frame += fps
				
			if int(self.current_frame) >= len(self.current_animation):
				self.current_frame = 0
					
			self.image = self.current_animation[int(self.current_frame)]

	def _check_tile_collisions(self, tiles):
		hit_list = []
		
		for tile in tiles:
			tile_rect = tile.rect
			if self.rect.colliderect(tile_rect):
				hit_list.append(tile_rect)

		return hit_list
		
	def _collide(self, tiles):
		collision_types = {"left": False, "right": False, "top": False, "bottom": False, "horizontal": False, "vertical": False}
		
		self.rect.x += self.movement[0]
		hit_list = self._check_tile_collisions(tiles)
		
		for tile in hit_list:
			if self.movement[0] > 0:
				self.rect.right = tile.left
				
				collision_types["right"] = True
				collision_types["horizontal"] = True
			elif self.movement[0] < 0:
				self.rect.left = tile.right
				
				collision_types["left"] = True
				collision_types["horizontal"] = True

		self.rect.y += self.movement[1]
		hit_list = self._check_tile_collisions(tiles)
		
		for tile in hit_list:
			if self.movement[1] > 0:
				self.rect.bottom = tile.top
				
				collision_types["bottom"] = True
				collision_types["vertical"] = True
			elif self.movement[1] < 0:
				self.rect.top = tile.bottom
				
				collision_types["top"] = True
				collision_types["vertical"] = True
				
		return collision_types
		
	def _translate(self, vel):
		self.movement[0] += vel[0]
		self.movement[1] += vel[1]
	
	def _update_movement(self):
		self.loc[0] = self.rect.x
		self.loc[1] = self.rect.y
		
		if self.flip_on_movement:
			if self.movement[0] > 0:
				self.flip = False
			elif self.movement[0] < 0:
				self.flip = True
		
		self.movement = [0, 0]
		
	def _kill(self):
		self.gone = True
		
	#Public methods
	
	def draw(self, surf, scroll):
		if self.image != None:
			surf.blit(pygame.transform.flip(self.image, self.flip, False), (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))