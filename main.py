import pygame
import timeit
from time import sleep
from pygame import *
from Map import Map
from Point import Point
from Multiplayer import Multiplayer
from threading import Thread, currentThread

size = (800, 600)

#### Класс игры
class RealSpace():

	def __init__(self):
		### Флаги
		self.run = True
		### Настройки
		self.nickname = 'Bit'
		self.font_size = 15
		### Счётчики и программные переменные
		self.draw_time = 1
		self.pressed_keys = []
		self.clock = pygame.time.Clock()
		self.lines = 0
		self.gui_text = []
		self.settings = self.load_settings()

		pygame.init()
		self.screen = pygame.display.set_mode(self.settings[0], DOUBLEBUF | RESIZABLE)

	def load_settings(self):
		try:
			file = open('text.txt', 'rt', 'utf-8')
		except:
			return [[800, 600], False]

	def __text_draw(self, text, font_size, color, x, y, gui_arr):
		font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
		text = font.render(text, 1, color)
		textpos = text.get_rect(x = x, y = y)
		gui_arr.append([text, textpos])
		#self.screen.blit(text, textpos)

	def __print(self, text, color, gui_arr):
		self.__text_draw(text, self.font_size, color, 10, (self.font_size + 2) * self.lines, gui_arr)
		self.lines += 1

	def setup(self):
		## Создаем карту
		self.game_map = Map(1000, 1000, 1000, 1000, self)
		self.mul = Multiplayer(self.game_map)
		## Создаем игрока
		self.game_map.spawnPlayer("player.png", self.nickname, 50)
		self.calc_thread = Thread(target=self.game_map.update)
		self.gui_thread = Thread(target=self.GUI)
		self.calc_thread.start()
		self.gui_thread.start()

	def GUI(self):
		t = currentThread()
		while getattr(t, "do_run", True):
			gui_arr = []
			self.lines = 0
			local = self.game_map.this_player.local.trunc()
			glob = self.game_map.this_player.glob.trunc()
			# Выводим время отрисовки и другую информацию
			self.__print(f'Local X { local.x }, Y { local.y } ', (255,0,0), gui_arr)
			self.__print(f'Global X { glob.x }, Y { glob.y } ', (255,0,0), gui_arr)
			self.__print(f'Draw time { self.draw_time :.6f} s', (255,0,0), gui_arr)
			self.__print(f'Iter time { self.game_map.itertime :.6f} s', (255,0,0), gui_arr) 
			self.__print(f'FPS { self.clock.get_fps() :.0f} ', (255,0,0), gui_arr)
			self.__print(f'Angle { self.game_map.this_player.angle :.0f}°', (255,0,0), gui_arr)
			self.__print(f'Angle speed { self.game_map.this_player.angle_speed :.0f}°', (255,0,0), gui_arr)
			self.__print(f'Speed { (self.game_map.this_player.vector * self.game_map.chunk).length() :.3f} ', (255,0,0), gui_arr)
			self.__print(f'Speed X { self.game_map.this_player.vector.x :.3f} Y { self.game_map.this_player.vector.y :.3f}', (255,0,0), gui_arr)
			self.gui_text = gui_arr
			#sleep(1 * 10 ** -1)

	def GUI_draw(self):
		for text in self.gui_text:
			self.screen.blit(text[0], text[1])

	def draw(self):
		# Рисуем
		self.game_map.draw()
		self.GUI_draw()

	def update(self):
		self.on_key_hold()

	def on_key_hold(self):
		for key in self.pressed_keys:
			self.game_map.this_player.on_key_hold(key)

	def on_key_press(self, key):
		self.pressed_keys.append(key)
		if key == pygame.K_ESCAPE:
			self.run = False

		if key == K_y:
			self.mul.start_server(9090)

		if key == K_u:
			self.mul.start_client('127.0.0.1', 9090)


		if key == K_f:
			if (self.settings[1]):
				self.screen = pygame.display.set_mode(self.settings[0], DOUBLEBUF | RESIZABLE)
			else:
				self.screen = pygame.display.set_mode(self.settings[0], FULLSCREEN | DOUBLEBUF | RESIZABLE)
			self.settings[1] = not self.settings[1]

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

	## Главный цикл
	def main(self):
		self.setup()
		while(self.run):
			## Вычисление событий
			self.events()
			## Вычисление
			self.update()
			draw_start_time = timeit.default_timer()
			## Заливка фона
			self.screen.fill([0, 0, 0])
			## Отрисовка
			self.draw()
			## Обновление экрана
			pygame.display.update()
			self.clock.tick()
			self.draw_time = timeit.default_timer() - draw_start_time

		self.mul.stop_server()
		self.mul.stop_client()
		self.calc_thread.do_run = self.run
		self.gui_thread.do_run = self.run
		self.calc_thread.join()
		self.gui_thread.join()
		pygame.quit()

game = RealSpace()
game.main()