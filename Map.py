import random
import pygame
import timeit
import time
from Object import Player

#### Карта
class Map:

	def __init__(self, w, h, chunk_w, chunk_h, game):
		self.game = game
		self.w = w
		self.h = h
		self.chunk_w = chunk_w
		self.chunk_h = chunk_h
		self.objects = []
		self.this_player = None
		self.itertime = 0
	### Спавн игрока
	def spawnPlayer(self, sprite, nickname, mass, x = None, y = None):
		## Создание спрайта
		player_sprite = pygame.image.load(sprite)
		player_sprite_width = player_sprite.get_width()
		player_sprite_height = player_sprite.get_height()
		## Создание игрока
		self.this_player = Player(player_sprite, mass, random.randint(player_sprite_width, (self.w * self.chunk_w) - player_sprite_width) / self.chunk_w, random.randint(player_sprite_height, (self.h * self.chunk_h) - player_sprite_height) / self.chunk_h, nickname, self)
		## Добавление игрока в список объектов
		self.objects.append(self.this_player)

	def update(self):
		while True:
			draw_start_time = timeit.default_timer()
			w = pygame.display.Info().current_w
			h = pygame.display.Info().current_h
			# Проходимся по всем обьектам и производим вычисления
			for obj in self.objects:
				obj.update(w, h)

			self.this_player.camera.update(w, h)
			self.itertime = timeit.default_timer() - draw_start_time
			time.sleep(1 / 60)

	def draw(self):
		self.this_player.camera.draw(self.game)