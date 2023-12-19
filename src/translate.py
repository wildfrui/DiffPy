from deep_translator import GoogleTranslator

class Translate:
	def translate_prompt(self, text):
		return GoogleTranslator(source='auto', target='english').translate(text)