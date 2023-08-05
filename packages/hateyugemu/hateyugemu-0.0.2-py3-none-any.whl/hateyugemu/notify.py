import requests

class LINENotifyBot:

	API_URL = "https://notify-api.line.me/api/notify"

	def __init__(self, token):
		self.headers = {'Authorization': 'Bearer ' + token}

	def send(self, msg):
		payload = {'message': msg}
		r = requests.post(self.API_URL, headers=self.headers, params=payload)