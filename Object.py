import pygame
import timeit
from Point import Point
from Camera import Camera

#### Класс объекта
class Object():

	def __init__(self, sprite, x, y, mass, game_map):
		self.type    = 'Object'			# Тип объекта
		self.sprite  = sprite			# Спрайт
		self.mass    = mass				# Масса
		self.glob    = Point(x, y)		# Координаты  в пространстве
		self.local   = Point()
		self.vector  = Point()			# Вектор движения
		self.game_map = game_map
		self.chunk   = Point(self.game_map.chunk_w, self.game_map.chunk_h)
	### Запускает движение по вектору
	def move(self, x, y):
		#new_x = Point(1, 0).rotate(self.sprite.angle)
		#new_y = Point(0, 1).rotate(self.sprite.angle)
		#self.vector = (new_x * x) + (new_y * y)
		self.vector += Point(x, y) / self.chunk

	def rotate(self, angle):
		self.sprite.angle += angle

	### Тут вычисляется все (Физика, Изменение обьектов, и прочее)
	def update(self, w, h):
		##################### ФИЗИКА #####################
		## Коллизия со стенами карты, кривая но пойдет
		# Если стенка по X
		if (self.glob.x <= (self.sprite.get_width() / self.game_map.chunk_w) and self.vector.x < 0.00):
			#self.vector.x = 0
			print('X jump')
			self.vector.x *= -1
		elif (self.glob.x >= self.game_map.w - (self.sprite.get_width() / self.game_map.chunk_w) and self.vector.x > 0.00):
			#self.vector.x = 0
			print('X jump')
			self.vector.x *= -1

		# Если стенка по Y
		if (self.glob.y <= (self.sprite.get_height() / self.game_map.chunk_h) and self.vector.y < 0.00):
			#self.vector.y = 0
			print('Y jump')
			self.vector.y *= -1
		elif (self.glob.y >= self.game_map.h - (self.sprite.get_height() / self.game_map.chunk_h) and self.vector.y > 0.00):
			#self.vector.y = 0
			print('Y jump')
			self.vector.y *= -1 
		
		## Инерция
		# TODO тут все криво, оставляю это тебе
		# self.vector это вектор прибавляющийся к координатам каждую итерацию
		# с помощью self.inert я хотел сделать угасание вектора но я ж кривожопый
		'''
		if (self.moving == 0):
			if (self.vector - self.inert != 0):
				self.vector -= self.inert
			elif (self.vector != 0):
				self.vector = Point()
		else:'''

		## Вычисляю новые координаты
		self.glob += self.vector
		#self.vector += (self.vector * math.pow(-1, 200))

	### Отрисовка
	def draw(self, coord, game):
		##################### ОТРИСОВКА #####################
		## Отрисовка спрайта
		sprite_rect = self.sprite.get_rect()
		game.screen.blit(self.sprite, (coord.x - (self.sprite.get_width() / 2), coord.y - (self.sprite.get_height() / 2)), sprite_rect)
		#vector = self.vector * Point(self.game_map.chunk_w, self.game_map.chunk_h)
		## Отрисовка вектора в виде линии
		#arcade.draw_line(coord.x, coord.y, coord.x + (vector.x * 5), coord.y + (vector.y * 5), arcade.color.WHITE, 1)


	### Скорость
	def speed(self):
		return self.vector.lenght()

	def on_key_hold(self, key):
		if key == pygame.K_w:
			self.move(0, -0.1)

		if key == pygame.K_s:
			self.move(0, 0.1)

		if key == pygame.K_a:
			self.move(-0.1, 0)

		if key == pygame.K_d:
			self.move(0.1, 0)

		if key == pygame.K_q:
			self.rotate(1)

		if key == pygame.K_e:
			self.rotate(-1)

#### Класс игрока
class Player(Object):

	def __init__(self, sprite, mass, x, y, nickname, game_map):
		super().__init__(sprite, x, y, mass, game_map)
		self.type     = 'Player'
		self.nickname = nickname
		self.camera   = Camera(game_map)

	def update(self, w, h):
		super().update(w, h)
		self.camera.setCamera(self.glob.x, self.glob.y)