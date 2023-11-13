import pymysql
from server_config import *


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

	def get_func_name(self, key):
		with self.con.cursor() as cur:
			cur.execute(f'SELECT func FROM variables WHERE phrase="{key}";')
			a = [x for x in cur.fetchall()]
			if len(a) > 0:
				return a[0]['func']
			return None


if __name__ == '__main__':
	a = DataBase()
	print(a.get_variables())
