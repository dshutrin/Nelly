import socket

from fuzzywuzzy.fuzz import ratio as rat
from threading import Thread
from config import *
from server_database import DataBase


class Server:
	def __init__(self):
		self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serv.bind((IP, PORT))
		self.serv.listen()
		self.base = DataBase()

	def sender(self, user, text: str):
		user.send(text.encode('utf-8'))

	def connection_processing(self, user):
		running = True
		while running:
			try:

				data = user.recv(1024).decode('utf-8')
				variables = self.base.get_variables()

				max_per = 0
				ans = None

				for variable in variables:
					per = rat(variable, data)
					if 70 < per > max_per:
						max_per = per
						ans = variable

				if ans:
					func_name = self.base.get_func_name(ans)
					if not func_name:
						func_name = 'None'
					self.sender(user, func_name)
				else:
					self.sender(user, 'None')

			except Exception as e:
				running = False

	def accept_connections(self):
		while True:
			con, addr = self.serv.accept()
			Thread(target=self.connection_processing, args=(con, )).start()

	def run(self):
		self.accept_connections()


if __name__ == '__main__':
	Server().run()
