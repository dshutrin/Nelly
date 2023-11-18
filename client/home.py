import serial.tools.list_ports
import serial
from time import sleep
from threading import Thread


class ArduinoConnect:
	def __init__(self, speed=115200):
		self.ser = serial.Serial('COM5', speed, timeout=1)
		sleep(3)
		print('connected!')

	def port_arduino(self):
		# Функция, чтобы узнать порт, где находиться Ардуино
		for port in list(serial.tools.list_ports.comports()):
			'''port.device, port.manufacturer, port.description'''
			if port.device:
				return port.device

	def arduino_write(self, data):
		# Функция для подключения и передачи файлов на ардуино
		if self.ser.isOpen():
			self.ser.write(bytes(data, encoding='utf-8'))
			sleep(0.5)

	def arduino_read(self):
		# Функция для подключения и получения файлов из ардуино
		if self.ser.isOpen():
			data = self.ser.read_all()
			print(data.decode('utf-8'))


if __name__ == '__main__':
	ino = ArduinoConnect()
	ino.arduino_write('PinOn 3')
	ino.arduino_read()
