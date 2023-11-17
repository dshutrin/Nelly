import socket
from functools import lru_cache
from fuzzywuzzy.fuzz import ratio as rat
from threading import Thread
import numpy as np
from face_recognition import face_distance

from server_config import *
from server_database import DataBase


class Server:
	def __init__(self):
		self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serv.bind((IP, PORT))
		self.serv.listen()
		self.base = DataBase()

	def sender(self, user, text: str):
		user.send(text.encode('utf-8'))

	@lru_cache
	def get_answer(self, data):
		variables = self.base.get_variables()

		max_per = 0
		ans = None

		for variable in variables:
			per = rat(variable, data)
			if 70 < per > max_per:
				max_per = per
				ans = variable
		return ans

	def get_message(self, user):
		total_data = bytes()
		data = user.recv(1024)
		total_data += data
		while True:
			data = user.recv(1024)
			total_data += data
			if len(data) < 1024:
				return total_data.decode('utf-8')

	def connection_processing(self, user):
		running = True
		while running:
			try:
				data = self.get_message(user)

				if data.startswith('get_user_name->'):
					data = np.array(eval(data.split('->')[1]))
					user_names = self.base.get_all_user_names()

					max_coef = 0
					ans_user_name = None
					for user_name in user_names:
						user_photos = self.base.get_user_photos(user_name)

						for user_photo in user_photos:
							coef = (1 - face_distance([data], user_photo)[0]) * 100
							if 55 < coef > max_coef:
								max_coef = coef
								ans_user_name = user_name

					if ans_user_name:
						self.sender(user, ans_user_name)
					else:
						self.sender(user, 'unknown user')

				else:
					ans = self.get_answer(data)

					if ans:
						func_name = self.base.get_func_name(ans)
						if not func_name:
							func_name = 'None'
						self.sender(user, func_name)
					else:

						if 'погода' in data.lower():
							self.sender(user, 'weather')
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
