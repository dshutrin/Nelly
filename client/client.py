import socket

# тестовые настройки
from config import *


class Client:
	def __init__(self, username=''):
		self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cli.connect((IP, PORT))
		self.username = username

	def set_user(self, username):
		self.username = username

	def sender(self, text: str):
		if text.startswith('['):
			self.cli.send(text.encode('utf-8'))
		else:
			self.cli.send(f'{self.username}: {text}'.encode('utf-8'))

	def get_user_name_by_photo(self, data):
		self.sender('get_user_name')
		self.sender(f'[{data}]')
		server_answer = self.cli.recv(1024).decode('utf-8')
		return server_answer

	def get_func_name(self, text):
		self.sender(text)
		server_answer = self.cli.recv(1024).decode('utf-8')
		return server_answer

	def up_user_trust_lvl(self, user_name):
		self.sender(f'up_trust_lvl->{user_name}')
