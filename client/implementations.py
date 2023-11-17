import datetime
from random import choice, randint as rd

import requests
import pygame
from bs4 import BeautifulSoup
from os import system as s


class Functions:

	# self.client.up_user_trust_lvl(current_user) -> повысить уровень доверия
	# self.client.down_user_trust_lvl(current_user) -> понизить уровень доверия

	def hello(self, task, current_user):
		vars = (
			'Рад встрече', 'Привет', 'Здравствуйте'
		)
		if rd(0, 10) in (1, 2, 3, 4, 5):
			self.say(choice(vars))
		else:
			self.say(choice(vars) + f' {current_user}')

	def bye(self, task, current_user):
		vars = (
			'До скорых встреч', 'Пока', 'До свидания'
		)
		self.say(choice(vars))

	def get_joke(self, task, current_user):
		r = requests.get(self.jokes_url)
		soup = BeautifulSoup(r.content, "html.parser")
		jokes = soup.find_all('div', class_="text")
		jokes = [x.text.strip() for x in jokes]
		self.say(choice(jokes))

	def start_music(self, task, current_user):
		tracks = [
			"Space_cruise.mp3", "Tank!.mp3",
			"creep.mp3", "Drive.mp3", "Without_me.mp3",
			"Where_is_my_mind.mp3"]  # Треки находятся в папке Music, сюда только назавние.расширение
		path = "Music\\" + choice(tracks)
		pygame.mixer.music.load(path)
		pygame.mixer.music.set_volume(100)

		self.say('На, слушай')
		pygame.mixer.music.play(1)

	def stop_music(self, task, current_user):
		pygame.mixer.music.stop()

	def weather(self, town, current_user):
		dels = ('погода', 'какая', 'в')
		for dl in dels:
			town = town.replace(dl, '').strip()

		if town:
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

			reqs = requests.get(
				f'https://www.google.com/search?q={town} погода&oq={town} погода&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
				headers=headers)

			soup = BeautifulSoup(reqs.text, 'html.parser')
			weather = soup.select('#wob_tm')[0].getText().strip()

			self.say(f'Температура воздуха в городе {town}: {weather}°C')
		else:
			self.say('Ты внятнее можешь сказать?')

	def get_time(self, task, current_user):
		time = str(datetime.datetime.now()).split()[1]
		time = f'{time.split(":")[0]}:{time.split(":")[1]}'
		self.say(time)

	def shutdown(self, task, current_user):
		s('shutdown /s /f /t 30')
		self.say(choice(
			['Ну пока, чо', 'Лови флэшку, кидаала']
		))
