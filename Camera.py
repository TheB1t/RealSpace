import pygame
import math
from Point import Point

#### Камера
class Camera:

	def __init__(self, game_map):
		self.game_map = game_map
		self.coord = Point(0, 0)
		self.chunk = Point(self.game_map.chunk_w, self.game_map.chunk_h) # Размер чанка
		self.new_grid = Point()
		self.invert_new_grid = Point()
		self.lines = []

	def setCamera(self, x, y):
		self.coord = Point(x, y)

	def update(self, w, h):
		screen = Point(w, h) / self.chunk
		half_screen = screen / 2 # Вычисление половины экрана в глобальных координатах
		self.new_grid = self.coord - half_screen # Вычисление сдвига координатной сетки(Левый нижний угол)
		self.invert_new_grid = self.coord + half_screen # Вычисление сдвига координатной сетки(Правый верхний)
		chunks = (self.invert_new_grid - self.new_grid).trunc() # Сколько чанков помещается на экране
		chunks_draw = (self.new_grid.trunc() - self.new_grid) * self.chunk # Переменная для отрисовки линий чанков

		self.lines = []

		# Отрисовка линий чанков по X
		for i in range(chunks.x + 2):
			new_x = chunks_draw.x + (self.game_map.chunk_w * i)
			self.lines.append([[new_x, 0], [new_x, h]])

		# Отрисовка линий чанков по Y
		for i in range(chunks.y + 2):
			new_y = chunks_draw.y + (self.game_map.chunk_h * i)
			self.lines.append([[0, new_y], [w, new_y]])

	def draw(self, game):
		for line in self.lines:
			pygame.draw.line(game.screen, (255, 255, 255), line[0], line[1], 1)

		# Отрисовка обьектов в поле видимости камеры
		for obj in self.game_map.objects:
			if (obj.glob > self.invert_new_grid) and (obj.glob < self.new_grid):
				new_coord = (obj.glob - self.new_grid) * self.chunk
				obj.draw(new_coord, game)