from random import choice

import requests
import pygame
import random
from bs4 import BeautifulSoup
from time import sleep
import os


class Functions:
	def hello(self):
		vars = (
			'Рад встрече', 'Привет', 'Здравствуйте'
		)
		self.say(choice(vars))

	def bye(self):
		vars = (
			'До скорых встреч', 'Пока', 'До свидания'
		)
		self.say(choice(vars))

	def get_joke(self):
		r = requests.get(self.jokes_url)
		soup = BeautifulSoup(r.content, "html.parser")
		jokes = soup.find_all('div', class_="text")
		jokes = [x.text.strip() for x in jokes]
		self.say(choice(jokes))

	def start_music(self):
		tracks = [
			"Space_cruise.mp3", "Tank!.mp3",
			"creep.mp3", "Drive.mp3", "Without_me.mp3",
			"Where_is_my_mind.mp3"]  # Треки находятся в папке Music, сюда только назавние.расширение
		path = "Music\\" + choice(tracks)
		pygame.mixer.music.load(path)
		pygame.mixer.music.set_volume(100)

		self.say('На, слушай')
		pygame.mixer.music.play(1)

	def stop_music(self):
		pygame.mixer.music.stop()
