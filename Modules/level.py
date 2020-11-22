import pygame, csv, random
pygame.init()
from pygame.locals import *

from Data.Modules.tile import Tile
from Data.Modules.player import Player

from Data.Modules.bullet import Bullet

from Data.Modules.cheri import Cheri
from Data.Modules.palta import Palta
from Data.Modules.manggo import Manggo
from Data.Modules.daidai import Daidai
from Data.Modules.limon import Limon

class Level(object):
	def __init__(self, tiles_file, floor_tiles_file, tileset, tile_size, player_loc):
		self.tiles_file = tiles_file
		self.floor_tiles_file = floor_tiles_file
		
		self.tileset = tileset

		self.tile_size = tile_size
		self.floor_tiles = []
		self.tiles = []
		self._load_tilemap()
		
		self.enemies = []
		self.enemy_bullets = []
		
		self.true_scroll = [200, 200]
		self.scroll = [0, 0]
		
		self.player = Player(player_loc)
		
		self.reset_value = 200
		self.timer = self.reset_value
		
		self.menu_state = "main_menu"
		
		self.score = 0
		
		self.level_started = False
		self.game_over = False
		
		self.win_sound = pygame.mixer.Sound("Data/Sounds/score_achieve.wav")
		pygame.mixer.Sound.set_volume(self.win_sound, 0.5)
		
	#Private methods
	
	def _load_tilemap(self):
		with open(self.tiles_file, newline = "") as tiles_file:
			tiles_reader = csv.reader(tiles_file)
			tiles_data = list(tiles_reader)
			
		tiles_y = 0
		for row in tiles_data:
			tiles_x = 0
			for tile in row:
				if tile != "-1":
					self.tiles.append(Tile([tiles_x * self.tile_size, tiles_y * self.tile_size], self.tileset, self.tile_size, int(tile)))
				tiles_x += 1
			tiles_y += 1
			
		with open(self.floor_tiles_file, newline = "") as floor_file:
			floor_reader = csv.reader(floor_file)
			floor_tiles_data = list(floor_reader)
			
		floor_y = -1
		for row in floor_tiles_data:
			floor_x = 0
			for tile in row:
				if tile != "-1":
					self.floor_tiles.append(Tile([floor_x * self.tile_size, floor_y * self.tile_size], self.tileset, self.tile_size, int(tile)))
				floor_x += 1
			floor_y += 1
			
	def _add_enemies(self):
		self.timer -= 1
				
		if self.timer <= 0:
			if len(self.enemies) < 9:
				enemy_x, enemy_y = random.randint(68, 1000), random.randint(68, 1000)
				enemy_type = random.randint(0, 4)
				
				enemy = None
				
				if enemy_type == 0:
					enemy = Cheri([enemy_x, enemy_y])
				elif enemy_type == 1:
					enemy = Palta([enemy_x, enemy_y])
				elif enemy_type == 2:
					enemy = Manggo([enemy_x, enemy_y])
				elif enemy_type == 3:
					enemy = Daidai([enemy_x, enemy_y])
				elif enemy_type == 4:
					enemy = Limon([enemy_x, enemy_y])
								
				self.enemies.append(enemy)

				if self.reset_value >= 10:
					self.reset_value -= 10

			self.timer = self.reset_value

	def _set_scroll(self):
		display_size = pygame.display.get_window_size()
		
		self.true_scroll[0] += (self.player.loc[0] - self.true_scroll[0] - display_size[0] / 2 + self.player.width / 2) / 15
		self.true_scroll[1] += (self.player.loc[1] - self.true_scroll[1] - display_size[1] / 2 + self.player.height / 2) / 15
		
		self.scroll = self.true_scroll.copy()
		self.scroll[0] = int(self.scroll[0])
		self.scroll[1] = int(self.scroll[1])
		
	def _render_text(self, text, size):
		font = pygame.font.Font("Data/Fonts/perfect_dos_vga.ttf", size)
		
		return font.render(text, True, (255, 255, 255))
		
	def _render_hud_text(self, text, size):
		font = pygame.font.Font("Data/Fonts/perfect_dos_vga.ttf", size)
		
		return font.render(text, True, (255, 255, 255), (0, 0, 0))
		
	def _render_start_menu(self, surf):
		surf.blit(self._render_text("Fruitshot", 70), (50, 50))
		surf.blit(self._render_text("A submission for Game Off 2020 by Kwago Games", 20), (50, 110))
		surf.blit(self._render_text("(Made using pygame)", 15), (50, 140))

		surf.blit(self._render_text("HOW TO PLAY:", 40), (50, 200))
		surf.blit(self._render_text("All of a sudden, in a grass field in which you live nearby, cute", 16), (50, 235))
		surf.blit(self._render_text("but deadly fruits suddenly appeared out of nowhere!", 16), (50, 250))
		surf.blit(self._render_text("The fruits caused chaos to anyone nearby their field and it is", 16), (50, 265))
		surf.blit(self._render_text("now up to you to stop them!", 16), (50, 280))
		surf.blit(self._render_text("You can attack the fruits by using the balls you have with you.", 16), (50, 295))
		surf.blit(self._render_text("Left-click to throw one! These balls have the ability to defeat", 16), (50, 310))
		surf.blit(self._render_text("fruits and increase your score when doing so! But beware,", 16), (50, 325))
		surf.blit(self._render_text("once a ball bounces off a wall or off an enemy, it will", 16), (50, 340))
		surf.blit(self._render_text("become harmful and damage you when collided with! So be", 16), (50, 355))
		surf.blit(self._render_text("careful about that.", 16), (50, 370))
		surf.blit(self._render_text("The fruits will appear on the screen and will start to attack you", 16), (50, 385))
		surf.blit(self._render_text("with bullets. Keep your dodging skills sharp - for a lot of these", 16), (50, 400))
		surf.blit(self._render_text("bullets will appear! Oh, and to move use the WASD keys.", 16), (50, 415))
		surf.blit(self._render_text("Good luck, player!", 16), (50, 450))

		surf.blit(self._render_text("Right-click to view the credits screen, or middle click to view", 18), (50, 500))
		surf.blit(self._render_text("the fruits catalog!", 18), (50, 518))
		surf.blit(self._render_text("Left-click to start the game!", 30), (50, 580))
		
	def _render_credits_menu(self, surf):
		surf.blit(self._render_text("Fruitshot", 20), (50, 23))
		surf.blit(self._render_text("Submission for Game Off 2020 by Kwago Games", 20), (50, 46))
		
		surf.blit(self._render_text("Made with Pygame 2.0.0 and Python 3.9.0", 16), (50, 100))
		
		surf.blit(self._render_text("Music obtained from https://www.zapsplat.com", 16), (50, 130))
		surf.blit(self._render_text("Art made by me using Pixelorama, paint.net and Slate", 16), (50, 145))
		surf.blit(self._render_text("Sound effects made with BFXR", 16), (50, 160))
		surf.blit(self._render_text("(P.S Check out my sister's Youtube at", 16), (50, 175))
		surf.blit(self._render_text("https://www.youtube.com/channel/UCr0XVqBl-kfShM1eOkhaHjA", 16), (50, 190))
		surf.blit(self._render_text("she helped me with some of the art :D)", 16), (50, 205))
		
		surf.blit(self._render_text("Right-click to go back to the main menu", 25), (50, 580))
		
	def _render_fruits_catalog(self, surf):
		cheri_img = pygame.image.load("Data/Sprites/Enemy_Anims/Cheri/idle/1.png").convert()
		palta_img = pygame.image.load("Data/Sprites/Enemy_Anims/Palta/idle/0.png").convert()
		manggo_img = pygame.image.load("Data/Sprites/Enemy_Anims/Manggo/idle/0.png").convert()
		limon_img = pygame.image.load("Data/Sprites/Enemy_Anims/Limon/idle/0.png").convert()
		daidai_img = pygame.image.load("Data/Sprites/Enemy_Anims/Daidai/idle/0.png").convert()
		
		cheri_img.set_colorkey((0, 0, 0))
		palta_img.set_colorkey((0, 0, 0))
		manggo_img.set_colorkey((0, 0, 0))
		limon_img.set_colorkey((0, 0, 0))
		daidai_img.set_colorkey((0, 0, 0))
	
		surf.blit(cheri_img, (10, 20))
		surf.blit(self._render_text("Cheri - A cute, bouncy cherry!", 20), (75, 45))
		
		surf.blit(palta_img, (10, 100))
		surf.blit(self._render_text("Palta - An avocado. Its skill at aiming is mediocre.", 20), (70, 125))

		surf.blit(manggo_img, (10, 250))
		surf.blit(self._render_text("Manggo - A mango. Believes that two bullets are", 20), (70, 265))
		surf.blit(self._render_text("better than one.", 20), (70, 284))

		surf.blit(limon_img, (10, 400))
		surf.blit(self._render_text("Limon - A lemon. Its attack is as sour as a lemon", 20), (80, 415))
		surf.blit(self._render_text("is.", 20), (80, 430))

		surf.blit(daidai_img, (10, 500))
		surf.blit(self._render_text("Daidai - An orange. It's good source of Vitamin", 20), (80, 515))
		surf.blit(self._render_text("C!", 20), (80, 530))
		
		surf.blit(self._render_text("Middle-click to go back to the main menu", 20), (50, 600))
		
	def _render_hud(self, surf):
		surf.blit(self._render_hud_text("HEALTH: " + str(self.player.health), 20), (20, 20))
		surf.blit(self._render_hud_text("SCORE: " + str(self.score), 20), (300, 20))
		
	def _render_game_over(self, surf):
		surf.blit(self._render_hud_text("GAME OVER!", 80), (70, 200))
		surf.blit(self._render_hud_text("Score: " + str(self.score), 50), (70, 500))
		surf.blit(self._render_hud_text("Left-click to retry!", 30), (70, 550))
		
		pygame.mixer.music.fadeout(100)

			
	#Public methods
	def get_player_input(self, event):
		if self.level_started:
			if not self.game_over:
				self.player.get_input(event, self.scroll)
		
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				if not self.level_started:
					if self.menu_state == "main_menu":
						pygame.mixer.music.play(-1)
						self.level_started = True
				else:
					if self.game_over:
						self.game_over = False
						self.menu_state = "main_menu"
						self.level_started = False
			
			elif event.button == 2:
				if self.menu_state == "main_menu":
					self.menu_state = "fruits_catalog"
				elif self.menu_state == "fruits_catalog":
					self.menu_state = "main_menu"

			elif event.button == 3:
				if self.menu_state == "main_menu":
					self.menu_state = "credits"
				elif self.menu_state == "credits":
					self.menu_state = "main_menu"

	def update_level(self):
		if self.level_started:
			if self.player.gone:
				self.game_over = True

			if not self.game_over:
				self._add_enemies()
				self.player.update(self.tiles, self.enemies, self.enemy_bullets)
					
				for i, enemy in sorted(enumerate(self.enemies), reverse = True):
					if not enemy.gone:
						enemy.update(self.tiles, self.player, self.enemy_bullets)
					else:
						pygame.mixer.Sound.play(self.win_sound)
						self.score += 500
						self.enemies.pop(i)
						
				for i, bullet in sorted(enumerate(self.enemy_bullets), reverse = True):
					if not bullet.gone:
						bullet.update(self.tiles)
					else:
						self.enemy_bullets.pop(i)
						
		self._set_scroll()

	
	def render_level(self, surf):
		for tile in self.floor_tiles:
			tile.draw(surf, self.scroll)
		
		for tile in self.tiles:
			tile.draw(surf, self.scroll)
			
		for enemy in self.enemies:
			enemy.draw(surf, self.scroll)
			
		for bullet in self.enemy_bullets:
			bullet.draw(surf, self.scroll)
			
		self.player.draw(surf, self.scroll)
		
		if not self.level_started:
			if self.menu_state == "main_menu":
				self._render_start_menu(surf)
			elif self.menu_state == "credits":
				self._render_credits_menu(surf)
			elif self.menu_state == "fruits_catalog":
				self._render_fruits_catalog(surf)
		else:
			if not self.game_over:
				self._render_hud(surf)
			else:
				self._render_game_over(surf)

