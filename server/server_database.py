import pymysql
from functools import lru_cache
from server_config import *
import numpy as np


class DataBase:
	def __init__(self):
		self.con = pymysql.connect(
			database=DB_NAME,
			user=USERNAME,
			password=PASSWORD,
			host=HOST,
			cursorclass=pymysql.cursors.DictCursor
		)

	def get_variables(self):
		with self.con.cursor() as cur:
			cur.execute('SELECT phrase FROM variables;')
			return [list(x.values())[0] for x in cur.fetchall()]

	@lru_cache
	def get_func_name(self, key):
		with self.con.cursor() as cur:
			cur.execute(f'SELECT func FROM variables WHERE phrase="{key}";')
			a = [x for x in cur.fetchall()]
			if len(a) > 0:
				return a[0]['func']
			return None

	def add_user_photos(self, user_name, encoded_list):
		with self.con.cursor() as cur:

			cur.execute(f'select id from users where name="{user_name}";')
			user_id = cur.fetchall()[0]['id']
			print(user_id)

			for data in encoded_list:
				cur.execute(f'insert into encoded_photos(user_id, encoded_data) values({user_id}, "{str(data)}");')
			self.con.commit()

	def get_user_photos(self, user_name):
		with self.con.cursor() as cur:
			cur.execute(f'select id from users where name="{user_name}";')
			user_id = cur.fetchall()[0]['id']

			cur.execute(f'select encoded_data from encoded_photos where user_id="{user_id}";')
			photos = cur.fetchall()
			return [
				np.array(eval(x['encoded_data']))
				for x in photos
			]

	def get_all_user_names(self):
		with self.con.cursor() as cur:
			cur.execute(f'select name from users;')
			return [x['name'] for x in cur.fetchall()]

	def up_trust_lvl(self, user_name):
		with self.con.cursor() as cur:
			cur.execute(f'select trust_lvl from users where name="{user_name}";')
			a = [x['trust_lvl'] for x in cur.fetchall()]
			if len(a):
				lvl = a[0]
				cur.execute(f'update users set trust_lvl={lvl+5} where name="{user_name}";')
				self.con.commit()

	def down_trust_lvl(self, user_name):
		with self.con.cursor() as cur:
			cur.execute(f'select trust_lvl from users where name="{user_name}";')
			a = [x['trust_lvl'] for x in cur.fetchall()]
			if len(a):
				lvl = a[0]
				cur.execute(f'update users set trust_lvl={lvl-5} where name="{user_name}";')
				self.con.commit()

	def get_user_by_name(self, username):
		with self.con.cursor() as cur:
			cur.execute(f'select * from users where name="{username}";')
			a = [x['id'] for x in cur.fetchall()]
			if len(a):
				return a[0]
			return None

	def get_home_instances(self, user_id):
		with self.con.cursor() as cur:
			cur.execute(f'select * from home_instances where user_id={user_id};')
			return [x for x in cur.fetchall()]


if __name__ == '__main__':
	a = DataBase()
	print(a.up_trust_lvl('dshutrin'))
