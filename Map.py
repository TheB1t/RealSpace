import pygame
import timeit
import time
import math
from Object import Player
from Point import Point
from threading import Thread, currentThread

#### Карта
class Map:

	def __init__(self, w, h, chunk_w, chunk_h, game):
		self.game = game
		self.w = w
		self.h = h
		self.chunk = Point(chunk_w, chunk_h)
		self.objects = []
		self.this_player = None
		self.itertime = 0

	def addObject(self, obj):
		self.objects.append(obj)
		return len(self.objects) - 1
	### Спавн игрока
	def spawnPlayer(self, sprite, nickname, mass, x = None, y = None):
		## Создание спрайта
		#player_sprite = pygame.transform.scale(player_sprite, (math.trunc(player_sprite.get_width() / 2), math.trunc(player_sprite.get_height() / 2)))
		## Создание игрока
		self.this_player = Player(sprite, mass, nickname, self, 5.0, 5.0)
		## Добавление игрока в список объектов
		self.addObject(self.this_player)

	def update(self):
		t = currentThread()
		while getattr(t, "do_run", True):
			draw_start_time = timeit.default_timer()
			w = pygame.display.Info().current_w
			h = pygame.display.Info().current_h
			# Проходимся по всем обьектам и производим вычисления
			for obj in self.objects:
				obj.update(w, h)

			self.this_player.camera.update(w, h)
			self.itertime = timeit.default_timer() - draw_start_time
			time.sleep(1 * 10 ** -300)

	def draw(self):
		self.this_player.camera.draw(self.game)