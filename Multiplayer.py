import socket
import json
from Object import Player
from Point import Point
from threading import Thread, currentThread

#### Мультиплеер
class Multiplayer:

	def __init__(self, game_map):
		self.game_map = game_map 			# Игровая карта
		self.socket = socket.socket() 		# Сокет
		self.userthreads = [] 				# Потоки подключенных игроков
		self.players = []
		self.server_thread = None 			# Поток сервера
		self.client_thread = None 			# Поток клиента

	### Серверная часть
	def server(self, port, max_conns):
		self.socket.bind(('0.0.0.0', port))
		self.socket.listen(max_conns)
		t = currentThread()
		while getattr(t, "do_run", True):
			conn, addr = self.socket.accept()
			conn.settimeout(10) 			# Таймаут соеденения
			user = Thread(target=self.update, args=(conn,))
			user.start()
			self.userthreads.append(user)

		for thr in self.userthreads:
			thr.do_run = False
			thr.join()

	### Клиентская часть
	def client(self, ip, port):
		self.socket.connect((ip, port))
		conn = self.socket
		conn.settimeout(10) 			# Таймаут соеденения
		data = conn.recv(3).decode("utf-8") 
		if (data == 'SUC'):
			conn.send(b'SUC')
			print(f'Connected to server { ip }')
			self.__client_side_init(conn)
			t = currentThread()
			while getattr(t, "do_run", True):
				self.__client_side(conn)
			sock.close()

	### Клиентский поток на сервере
	def update(self, conn):
		conn.send(b'SUC')
		data = conn.recv(3).decode("utf-8") 
		if (data == 'SUC'):
			player = self.__server_side_init(conn)
			print(player)
			t = currentThread()
			while getattr(t, "do_run", True):
				self.__server_side(conn, player)
			conn.close()

	### Запуск потока серверной части
	def start_server(self, port, max_conns = 20):
		self.server_thread = Thread(target=self.server, args=(port, max_conns,))
		self.server_thread.start()

	### Запуск потока клиентской части
	def start_client(self, ip, port):
		self.client_thread = Thread(target=self.client, args=(ip, port,))
		self.client_thread.start()

	### Остановка потока серверной части
	def stop_server(self):
		if (self.server_thread):
			self.server_thread.do_run = False
			self.server_thread.join()

	### Остановка потока клиентской части
	def stop_client(self):
		if (self.client_thread):
			self.client_thread.do_run = False
			self.client_thread.join()

	### Действия сервера после подключения игрока
	def __server_side_init(self, conn):
		data = conn.recv(1024).decode("utf-8")
		player = json.loads(data) 
		print(f'Connected player { player[6] }')
		# [self.spritefile, self.mass, self.angle, [self.glob.x, self.glob.y], [self.vector.x, self.vector.y]]
		this_player = Player(spritefile = player[0], mass = player[1], nickname = player[6], game_map = self.game_map, x = player[3][0], y = player[3][1])
		this_player.angle = player[2]
		this_player.vector = Point(player[4][0], player[4][1])
		self.game_map.addObject(this_player)
		self.players.append(this_player)
		conn.send(b'OK.')
		return len(self.players) - 1

	### Действия клиента после подключения к серверу
	def __client_side_init(self, conn):
		conn.send(str(self.game_map.this_player).encode('utf-8'))
		while conn.recv(3).decode("utf-8") != "OK.":
					pass


	### Основной цикл клиента
	def __client_side(self, conn):
		conn.send(str(self.game_map.this_player).encode('utf-8'))
		counter = 1
		while True:
			data = conn.recv(3).decode("utf-8") 
			if (data == "STO"):
				break;
			data = conn.recv(1024).decode("utf-8")
			obj = json.loads(data) 
			obj_data = self.game_map.objects
			if (counter >= len(obj_data)):
				if (obj[5] == "Object"):
					obj_data.append(Object(obj[0], obj[1], self.game_map, obj[3][0], obj[3][1]))
				elif (obj[5] == "Player"):
					obj_data.append(Player(obj[0], obj[1], obj[6], self.game_map, obj[3][0], obj[3][1]))
			else:
				obj_data[counter].glob = Point(obj[3][0], obj[3][1])
				obj_data[counter].angle = obj[2]
				obj_data[counter].vector = Point(obj[4][0], obj[4][1])
			counter += 1
			conn.send(b'OK.')

	### Основной цикл сервера
	def __server_side(self, conn, pla):
		data = conn.recv(1024).decode("utf-8")
		player = json.loads(data) 
		# [self.spritefile, self.mass, self.angle, [self.glob.x, self.glob.y], [self.vector.x, self.vector.y]]
		this_player = self.players[pla]
		this_player.glob = Point(player[3][0], player[3][1])
		this_player.angle = player[2]
		this_player.vector = Point(player[4][0], player[4][1])

		conn.send(b'STA')		
		for obj in self.game_map.objects:
			if (obj != this_player):
				conn.send(str(obj).encode('utf-8'))
				while conn.recv(3).decode("utf-8") != "OK.":
					pass

		conn.send(b'STO')
