import cv2
import time
from os import getcwd
from face_recognition import load_image_file, face_encodings

from client import Client


class Camera:
	def __init__(self):
		self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		for i in range(50):
			val, image = self.camera.read()
		time.sleep(0.1)

	def get_photo(self):
		for i in range(5):
			val, image = self.camera.read()
		cv2.imwrite(f"{getcwd()}/photos/who_is.jpg", image)


class FaceID:
	def __init__(self, client):
		self.cam = Camera()
		self.client = client

	def get_current_user_name(self):

		self.cam.get_photo()
		current_user = face_encodings(load_image_file(f"{getcwd()}/photos/who_is.jpg"))[0].tolist()
		data = ''
		for el in current_user:
			if data:
				data = f'{data}, {str(el)}'
			else:
				data = str(el)

		current_user_name = self.client.get_user_name_by_photo(data)
		return current_user_name
