from threading import Thread
from vosk import Model, KaldiRecognizer, SetLogLevel
from win32com.client import Dispatch as d

import pyaudio
import json
import pygame
import vk_api

from config import vk_token
from client import Client
from implementations import Functions
from social_networks import NetworkProcessor
from face_rec import FaceID, Camera


class Assistant(Functions, NetworkProcessor):
	def __init__(self):
		self.engine = d("SAPI.SpVoice")

		self.ASSIST_NAME = 'Нелли'

		SetLogLevel(-1)
		self.model = Model("model")
		self.rec = KaldiRecognizer(self.model, 48000)
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=8000)
		self.stream.start_stream()

		pygame.mixer.init()

		self.soc_nets_con = True  # подключение к соц сетям
		try:
			self.session = vk_api.VkApi(token=vk_token)
		except Exception as error:
			self.say('Я не смогла подключиться к VK!')
			self.soc_nets_con = False

		self.running = True
		self.jokes_url = "https://www.anekdot.ru/tags/%D0%A8%D1%82%D0%B8%D1%80%D0%BB%D0%B8%D1%86/?type=anekdots"
		self.client = Client()
		self.facer = FaceID(self.client)

		self.phrases = []
		self.create_threads()

		self.commands = {
			'hello': self.hello,
			'bye': self.bye,
			'get_joke': self.get_joke,
			'start_music': self.start_music,
			'stop_music': self.stop_music,
			'weather': self.weather,
			'get_time': self.get_time,
			'shutdown': self.shutdown
		}

	def create_threads(self):
		threads = (
			Thread(target=self.speech_processing),  # воспроизведение речи
			Thread(target=self.social_networks_processing)
		)
		for thread in threads:
			thread.start()

	def say(self, text):
		self.phrases.append(text)

	def speech_processing(self):
		while True:
			if len(self.phrases) > 0:
				self.engine.speak(self.phrases[0])
				del self.phrases[0]

	def listen(self):
		while True:
			data = self.stream.read(4000, exception_on_overflow=False)
			if (self.rec.AcceptWaveform(data)) and (len(data) != 0):
				answer = json.loads(self.rec.Result())
				if answer["text"]:
					yield answer["text"].lower()

	def run(self):
		for task in self.listen():
			print(task)
			func_name = self.client.get_func_name(task)
			print(func_name)
			current_user = self.facer.get_current_user_name()
			print(current_user)
			if func_name != 'None':
				if func_name in self.commands:
					self.commands[func_name](task, current_user)


if __name__ == '__main__':
	Assistant().run()
