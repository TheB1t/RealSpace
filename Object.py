import pygame
import timeit
import random
import json
import math
from Point import Point
from Camera import Camera

def randomXY(gmap, w, h):
	return (random.randint(w, (gmap.w * gmap.chunk.x) - w) / gmap.chunk.x, random.randint(h, (gmap.h * gmap.chunk.y) - h) / gmap.chunk.y)
#### Класс объекта
class Object():

	def __init__(self, spritefile, mass, game_map, x = None, y = None):
		self.type    = 'Object'									# Тип объекта
		self.spritefile = spritefile
		self.sprite  = pygame.image.load(spritefile)			# Спрайт
		self.mass    = mass										# Масса
		self.angle   = 0
		self.angle_speed = 0 # Момент вращения, град/тик
		self.game_map = game_map
		if (x == None or y == None):
			x, y = randomXY(self.game_map, self.sprite.get_width(), self.sprite.get_height())
		self.glob    = Point(x, y)								# Глобальные координаты (Чанк)
		self.local   = Point()									# Локальные координаты (В чанке)
		self.vector  = Point()									# Вектор движения
		self.deltatime = 1 / 60									# Тик

	### Запускает движение по вектору
	def move(self, x, y):
		# Новый вектор = Старый вектор + (((Вектор движения / Размер чанка) / Масса) * Дельта времени).rotate(Угол)
		self.vector += (((Point(x, y) / self.game_map.chunk) / self.mass) * self.deltatime).rotate(self.angle)

	### Устанавливает угол поворота
	def rotate(self, angle):
		a = (math.pi * angle) / 180
		self.angle_speed += (a * self.deltatime)

	### Тут вычисляется все (Физика, Изменение обьектов, и прочее)
	def update(self, w, h):
		self.local = (self.glob - self.glob.trunc()) * self.game_map.chunk
		##################### ФИЗИКА #####################
		## Коллизия со стенами карты, кривая но пойдет
		# Если стенка по X
		if (self.glob.x <= (self.sprite.get_width() / self.game_map.chunk.x) and self.vector.x < 0.00):
			#self.vector.x = 0
			print('X jump')
			self.vector.x *= -1
		elif (self.glob.x >= self.game_map.w - (self.sprite.get_width() / self.game_map.chunk.x) and self.vector.x > 0.00):
			#self.vector.x = 0
			print('X jump')
			self.vector.x *= -1

		# Если стенка по Y
		if (self.glob.y <= (self.sprite.get_height() / self.game_map.chunk.y) and self.vector.y < 0.00):
			#self.vector.y = 0
			print('Y jump')
			self.vector.y *= -1
		elif (self.glob.y >= self.game_map.h - (self.sprite.get_height() / self.game_map.chunk.y) and self.vector.y > 0.00):
			#self.vector.y = 0
			print('Y jump')
			self.vector.y *= -1 

		newangle = self.angle + (self.angle_speed / self.mass)
		if (newangle < -360):
			self.angle = 360 + newangle
		elif (newangle > 360):
			self.angle = 360 - newangle
		else:
			self.angle = newangle

		## Вычисляю новые координаты
		self.glob += self.vector
		#self.vector += (self.vector * math.pow(-1, 200))

	### Отрисовка
	def draw(self, coord, game):
		##################### ОТРИСОВКА #####################
		## Отрисовка спрайта
		new_sprite = pygame.transform.rotate(self.sprite, self.angle)
		sprite_rect = new_sprite.get_rect(center=(coord.x, coord.y))
		game.screen.blit(new_sprite, sprite_rect)
		vector = self.vector * self.game_map.chunk
		## Отрисовка вектора в виде линии
		pygame.draw.line(game.screen, (255, 255, 255), [coord.x, coord.y], [coord.x + (vector.x * 25), coord.y + (vector.y * 25)], 1)


	### Скорость
	def speed(self):
		return self.vector.lenght()

	### Действия при нажатой кнопке
	def on_key_hold(self, key):
		if key == pygame.K_w:
			self.move(0, -5)

		if key == pygame.K_s:
			self.move(0, 5)

		if key == pygame.K_a:
			self.move(-5, 0)

		if key == pygame.K_d:
			self.move(5, 0)

		if key == pygame.K_q:
			self.rotate(100)

		if key == pygame.K_e:
			self.rotate(-100)

	def __str__(self):
		data = [self.spritefile, self.mass, self.angle, [self.glob.x, self.glob.y], [self.vector.x, self.vector.y], self.type]
		return json.dumps(data)

#### Класс игрока
class Player(Object):
	def __init__(self, spritefile, mass, nickname, game_map, x = None, y = None):
		super().__init__(spritefile, mass, game_map, x, y)
		self.type     = 'Player'
		self.nickname = nickname
		self.camera   = Camera(game_map)

	def update(self, w, h):
		super().update(w, h)
		self.camera.setCamera(self.glob.x, self.glob.y)

	def __str__(self):
		data = json.loads(super().__str__())
		data.append(self.nickname)
		return json.dumps(data)