import os
import requests
import base64
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()
api_host = os.getenv('API_HOST')
api_key = os.getenv('DIFF_TOKEN')
engine_id = "stable-diffusion-xl-1024-v1-0"
generate_url = f"{api_host}/v1/generation/{engine_id}/text-to-image"

class PicGenerator:
	sizes = {"1:1": {"width": 1024, "height": 1024}, "5:12": {"width": 640, "height": 1536}, "7:9": {"width": 896, "height": 1152}, "9:7": {"width": 1152, "height": 896}}
	style_presets = ["3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art", "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound", "neon-punk", "origami", "photographic", "pixel-art", "tile-texture"]
	
	def __init__(self):
		self.prompt = None
		self.size = None
		self.style_preset = None
		self.pic = None
		self.last_request = None

	def set_last_request(self, prompt, style_preset, size):
		self.last_request = [prompt, style_preset, size]
  
	def get_last_request(self):
		return self.last_request
    
	def set_prompt(self, text):
		self.prompt = self.translate_prompt(text)
		print(self.prompt)
  
	def get_prompt(self):
		return self.prompt
	
	def set_pict_size(self, size):
		self.size = self.sizes[size]

	def get_pict_size(self):
		return self.size

	def set_pict_style(self, style):
		self.style_preset = style

	def get_pict_style(self):
		return self.style_preset

	def generate(self):
		response = requests.post(generate_url, headers={
			"Content-Type": "application/json",
       		"Accept": "application/json",
        	"Authorization": f"Bearer {api_key}"
		}, json= {
			"text_prompts": [
				{
					"text": self.prompt
				}
			],
			"cfg_scale": 7,
        	"height": self.size["height"],
       		"width": self.size["width"],
        	"samples": 1,
			"style_preset": self.style_preset,
        	"steps": 30,
		})
  
		if response.status_code != 200:
			raise Exception("Non-200 response: " + str(response.text))
		return response.json()

	def translate_prompt(self, text):
		return GoogleTranslator(source='auto', target='english').translate(text)
		
	def load(self):
		data = self.generate()
		pic = base64.b64decode(data["artifacts"][0]["base64"])
		self.set_last_request(self.get_prompt(), self.get_pict_style(), self.get_pict_size())
		return pic