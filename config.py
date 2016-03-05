import json


class Config:
	def __init__(self, filename):
		self.filename = filename


	def get(self):
		with open(self.filename, 'r') as file:
			config = json.load(file)

		return config
		