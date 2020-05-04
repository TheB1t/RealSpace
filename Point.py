import math

#### Вектора
class Point:

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	### Возвращает длину вектора
	def length(self):
		return math.sqrt((self.x * self.x) + (self.y * self.y))

	def norm(self):
		return Point(self.x / self.lenght(), self.y / self.lenght())
	
	def trunc(self):
		return Point(math.trunc(self.x), math.trunc(self.y))
	### Возвращает вектор повернутый на angle
	def rotate(self, angle):
		return Point((self.x * math.cos(angle)) - (self.y * math.sin(angle)), (self.x * math.sin(angle)) + (self.y * math.cos(angle)))

	### Вызывается при сложении Point += obj или Point + obj
	def __add__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			return Point(self.x + obj, self.y + obj)
		## Если obj обьект то
		else:
			return Point(self.x + obj.x, self.y + obj.y)

	### Вызывается при вычитании Point -= obj или Point - obj
	def __sub__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			return Point(self.x - obj, self.y - obj)
		## Если obj обьект то
		else:
			return Point(self.x - obj.x, self.y - obj.y)

	### Вызывается при умножении Point *= obj или Point * obj
	def __mul__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			return Point(self.x * obj, self.y * obj)
		## Если obj обьект то
		else:
			return Point(self.x * obj.x, self.y * obj.y)
			#return (self.x * self.y) + (obj.x * obj.y)

	### Вызывается при делении Point /= obj или Point / obj
	## По сути она нахуй не нужна
	def __truediv__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			return Point(self.x / obj, self.y / obj)
		## Если obj обьект то
		else:
			return Point(self.x / obj.x, self.y / obj.y)

	### Вызывается при Point != obj
	def __ne__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			if (self.x != obj) and (self.y != obj):
				return True
		## Если obj обьект то
		else:
			if (self.x != obj.x) and (self.y != obj.y):
				return True
		return False
	### Вызывается при Point == obj
	def __eq__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			if (self.x == obj) and (self.y == obj):
				return True
		## Если obj обьект то
		else:
			if (self.x == obj.x) and (self.y == obj.y):
				return True
		return False
	### Вызывается при Point < obj
	def __lt__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			if (self.x < obj) and (self.y < obj):
				return True
		## Если obj обьект то
		else:
			if (self.x < obj.x) and (self.y < obj.y):
				return True
		return False
	### Вызывается при Point > obj
	def __lt__(self, obj):
		## Если obj цифра то
		if isinstance(obj, int) or isinstance(obj, float):
			if (self.x > obj) and (self.y > obj):
				return True
		## Если obj обьект то
		else:
			if (self.x > obj.x) and (self.y > obj.y):
				return True
		return False

	def __str__(self):
		return str(self.x)+', '+str(self.y)