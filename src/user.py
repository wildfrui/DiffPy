import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
api_host = os.getenv('API_HOST')
api_key = os.getenv('DIFF_TOKEN')

user_url = f"{api_host}/v1/user/account"
balance_url = f"{api_host}/v1/user/balance"

class User:
	def get_user_info(self):
		response = requests.get(user_url, headers={
    		"Authorization": f"Bearer {api_key}"
		})
		payload = response.json()
		return payload

	def get_user_balance(self):
		response = requests.get(balance_url, headers={
    		"Authorization": f"Bearer {api_key}"
		})
		payload = response.json()
		return payload["credits"]