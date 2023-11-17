from vk_api.longpoll import VkLongPoll, VkEventType


class NetworkProcessor:
	def social_networks_processing(self):
		self.longpoll = VkLongPoll(self.session)
		print('Обработчик вк запущен!')
		connections_retried = 0

		try:

			for event in self.longpoll.listen():
				if event.type == VkEventType.MESSAGE_NEW:

					if event.from_user:
						sender_id = event.user_id

						sender_name = self.session.method('users.get', {'user_id': sender_id})
						sender_name = f'{sender_name[0]["first_name"]} {sender_name[0]["last_name"]}'

						self.say(f'Пользователь {sender_name} прислал вам новое сообщение!\nМожете его заигнорить!')

		except Exception as e:
			while connections_retried < 10:
				try:
					self.soc_nets_con = False
					self.say('Вк сейчас не доступен!\nЯ перестаю следить за обновлениями!')
				except Exception as e:
					connections_retried += 1

