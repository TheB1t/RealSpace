import pygame
import timeit
from pygame import *
from Map import Map
from Point import Point
from threading import Thread

size = (800, 600)

#### Класс игры
class RealSpace():

	def __init__(self):
		self.run = True
		self.fullscreen = False
		self.draw_time = 1
		self.pressed_keys = []
		self.nickname = 'Bit'

		pygame.init()
		self.screen = pygame.display.set_mode(size, DOUBLEBUF | RESIZABLE)

	def __text_draw(self, text, font_size, color, x, y):
		font = pygame.font.Font(None, font_size)
		text = font.render(text, 1, color)
		textpos = text.get_rect(x = x, y = y)
		self.screen.blit(text, textpos)

	def setup(self):
		## Создаем карту
		self.game_map = Map(1000, 1000, 100, 100, self)
		## Создаем игрока
		self.game_map.spawnPlayer("player.png", self.nickname, 500)
		thread1 = Thread(target=self.game_map.update)
		thread1.start()

	def draw(self):
		draw_start_time = timeit.default_timer()
		# Рисуем
		self.game_map.draw()
		# Выводим время отрисовки и другую информацию
		self.__text_draw(f'Coord X { self.game_map.this_player.glob.x }, Y { self.game_map.this_player.glob.y } ', 20, (255,0,0), 50, 45)
		self.__text_draw(f'Draw time { self.draw_time * 1000 :.6f} ms', 20, (255,0,0), 50, 65)
		#arcade.draw_text(f'Iters { self.game_map.itertime * 1000 } ', 15, 30, arcade.color.WHITE, 12)
		#arcade.draw_text(f'Draw time { self.draw_time * 1000 :.6f} ', 15, 15, arcade.color.WHITE, 12)
		self.draw_time = timeit.default_timer() - draw_start_time

	def update(self):
		self.on_key_hold()

	def on_key_hold(self):
		for key in self.pressed_keys:
			self.game_map.this_player.on_key_hold(key)

	def on_key_press(self, key):
		self.pressed_keys.append(key)
		if key == pygame.K_ESCAPE:
			self.run = False

		if key == K_f:
			if (self.fullscreen):
				self.screen = pygame.display.set_mode(size, DOUBLEBUF | RESIZABLE)
			else:
				self.screen = pygame.display.set_mode(size, FULLSCREEN | DOUBLEBUF | RESIZABLE)
			self.fullscreen = not self.fullscreen

	def on_key_release(self, key):
		del self.pressed_keys[self.pressed_keys.index(key)]

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False

			if event.type == pygame.KEYUP:
				self.on_key_release(event.key)

			if event.type == pygame.KEYDOWN:
				self.on_key_press(event.key)

	def main(self):
		self.setup()
		while(self.run):
			self.events()
			self.update()
			#screen.blit(image, (0, 0), cropRect)
			self.screen.fill([0, 0, 0])
			self.draw()
			pygame.display.update()
		pygame.quit()
 
 
game = RealSpace()
game.main()