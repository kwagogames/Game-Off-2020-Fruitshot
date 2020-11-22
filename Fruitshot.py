import pygame, sys
pygame.init()
from pygame.locals import *

from Data.Modules.player import Player
from Data.Modules.level import Level

pygame.display.set_icon(pygame.image.load("Data/Sprites/Enemy_Anims/Cheri/idle/1.png"))
display = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Fruitshot")

main_clock = pygame.time.Clock()

level = Level("Data/Maps/arena_tiles.csv", "Data/Maps/arena_floor.csv", "Data/Sprites/Tilesets/fruit_world_tileset.png", 64, [420, 420])

pygame.mixer.music.load("Data/Music/main_theme_zapsplat.mp3")
pygame.mixer.set_num_channels(100)

while True:
	display.fill((13, 40, 27))
		
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				if level.game_over:
					level = Level("Data/Maps/arena_tiles.csv", "Data/Maps/arena_floor.csv", "Data/Sprites/Tilesets/fruit_world_tileset.png", 64, [420, 420])
					
			
		level.get_player_input(event)
			
	level.update_level()
	level.render_level(display)

	pygame.display.update((0, 0, pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))
	main_clock.tick(60)
