import socket

# тестовые настройки
from config import *


class Client:
	def __init__(self):
		self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cli.connect((IP, PORT))

	def sender(self, text: str):
		self.cli.send(text.encode('utf-8'))

	def get_func_name(self, text):
		self.sender(text)
		server_answer = self.cli.recv(1024).decode('utf-8')
		return server_answer
