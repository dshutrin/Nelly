from face_recognition import load_image_file, face_encodings, face_distance
from os import getcwd, listdir, path
from server_database import DataBase


class Encoder:
	def __init__(self):
		self.BASE_DIR = getcwd()
		self.photo_path = path.join(self.BASE_DIR, 'photos')
		self.base = DataBase()

	def encode(self, name):
		names = listdir(self.photo_path)
		if name in names:
			cur_paths = [
				path.join(self.photo_path, name, path_) for path_ in listdir(path.join(self.photo_path, name))
			]

			output = []
			for path_ in cur_paths:
				output.append(
					face_encodings(load_image_file(path_))[0].tolist()
				)
			self.base.add_user_photos(name, output)

		else:
			return None


if __name__ == '__main__':
	e = Encoder()
	e.encode('Дмитрий')
	e.encode('Владимир Владимирович')
