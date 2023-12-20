import telebot
import os
from dotenv import load_dotenv
from telebot import types

from generate import PicGenerator
from user import User

load_dotenv()
bot_key = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_key)
pic = PicGenerator()
user = User()

# подумать где хранить длинный текст
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, "Привет! Я бот, который генерирует картинки по запросу!")
	markup = generate_keyboard_generation()
	bot.send_message(message.chat.id, "Выберите вариант взаимодействия с моделью:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def show_help(message):
	markup = generate_keyboard_generation()
	bot.send_message(message.chat.id, "Привет! Я могу тебе помочь", reply_markup=markup)

@bot.message_handler(commands=['balance'])
def show_balance(message):
	balance = user.get_user_balance()
	markup = generate_keyboard_generation()
	bot.send_message(message.chat.id, f"Доступно токенов: {balance}", reply_markup=markup)
 
@bot.message_handler(commands=['repeat'])
def repeat_prompt(message):
	global pic
	if pic.get_last_request() != None:
		get_saved_params(message, True)
	else:
		markup = generate_keyboard_generation()
		bot.send_message(message.chat.id, "Вы еще не делали запрос на генерацию изображения", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def input_prompt(message):
	if message.text == "Генерация изображения по тексту" or message.text == "Сгенерировать новое изображение":
		sent_msg = bot.send_message(message.chat.id, "Напишите текст, который хотите сгенерировать:", reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(sent_msg, choose_settings)
	if message.text == "Повторить предыдущий запрос":
		bot.send_message(message.chat.id, "Повторяю предыдущий запрос...")
		repeat_prompt(message)
		# bot.register_next_step_handler(sent_msg, repeat_prompt)
  
def choose_settings(message):
	global pic
	global pic
	if check_command(message):
		pic.set_prompt(message.text)
		if pic.get_last_request() != None:
			markup = generate_keyboard_save_settings()
			sent_msg = bot.send_message(message.chat.id, f"Использовать настройки из предыдущего запроса - {pic.get_last_request()[1]} {pic.get_last_request()[3]}?", reply_markup=markup)
			bot.register_next_step_handler(sent_msg, decide_next_step)
		else:
			choose_style(message)
      
def decide_next_step(message):
    if message.text == "Использовать настройки из предыдущего запроса":
        get_saved_params(message, False)
    if message.text == "Использовать новые настройки":
        choose_style(message)
        
def get_saved_params(message, need_prompt):
	if(need_prompt):
		pic.set_prompt(pic.get_last_request()[0])
	pic.set_pict_style(pic.get_last_request()[1])
	pic.size = pic.get_last_request()[2]
	bot.send_message(message.from_user.id, "Подождите пока я генерирую вашу картинку...",
						 reply_markup=types.ReplyKeyboardRemove())
	pic_binary = pic.load()
	bot.send_photo(message.from_user.id, photo=(pic_binary))
	markup = generate_keyboard_generation(repeatItem=True)
	bot.send_message(message.from_user.id, "Вы можете продолжить работать с ботом", reply_markup=markup)
        
def choose_style(message):
	global pic
	if check_command(message):
		markup = generate_keyboard_styles()
		sent_msg = bot.send_message(message.chat.id, "Выберите стиль:", reply_markup=markup)
		bot.register_next_step_handler(sent_msg, choose_size)
  
def choose_size(message):
	global pic
	if check_command(message):
		if message.text not in PicGenerator.style_presets:
			markup = generate_keyboard_styles()
			sent_msg = bot.send_message(message.chat.id, "Выберите стиль из предложенных", reply_markup=markup)
			bot.register_next_step_handler(sent_msg, choose_size)
		else:
			pic.set_pict_style(message.text)
			markup = generate_keyboard_sizes()
			sent_msg = bot.send_message(message.chat.id, "Выберите размер:", reply_markup=markup)
			bot.register_next_step_handler(sent_msg, generate_pic)

def generate_pic(message):
	global pic
	if check_command(message):
		if message.text not in PicGenerator.sizes:
			markup = generate_keyboard_sizes()
			sent_msg = bot.send_message(message.chat.id, "Выберите размер из предложенных", reply_markup=markup)
			bot.register_next_step_handler(sent_msg, generate_pic)
		else:
			pic.set_pict_size(message.text)
			bot.send_message(message.from_user.id, "Подождите пока я генерирую вашу картинку...", reply_markup=types.ReplyKeyboardRemove())
			pic_binary = pic.load()
			bot.send_photo(message.from_user.id, photo = (pic_binary))
			markup = generate_keyboard_generation(repeatItem=True)
			bot.send_message(message.from_user.id, "Вы можете продолжить работать с ботом", reply_markup=markup)

 
def generate_keyboard_styles():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('3d-model'), types.KeyboardButton('analog-film'), types.KeyboardButton(
        'anime'), types.KeyboardButton('cinematic'))
    markup.row(types.KeyboardButton('comic-book'), types.KeyboardButton('digital-art'), types.KeyboardButton(
        'enhance'), types.KeyboardButton('fantasy-art'))
    markup.row(types.KeyboardButton('isometric'), types.KeyboardButton('line-art'), types.KeyboardButton(
        'low-poly'), types.KeyboardButton('pixel-art'))
    markup.row(types.KeyboardButton('modeling-compound'), types.KeyboardButton('neon-punk'), types.KeyboardButton(
        'origami'), types.KeyboardButton('tile-texture'))
    return markup

def generate_keyboard_sizes():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('1:1'), types.KeyboardButton('5:12'), types.KeyboardButton(
        '7:9'), types.KeyboardButton('9:7') )
    return markup

def generate_keyboard_generation(repeatItem=False):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if repeatItem:
		item_1 = types.KeyboardButton("Сгенерировать новое изображение")
		item_2 = types.KeyboardButton("Повторить предыдущий запрос")
		markup.add(item_1, item_2)
	else:
		item = types.KeyboardButton("Генерация изображения по тексту")
		markup.add(item)
	return markup

def generate_keyboard_save_settings():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item_1 = types.KeyboardButton("Использовать настройки из предыдущего запроса")
	item_2 = types.KeyboardButton("Использовать новые настройки")
	markup.add(item_1, item_2)
	return markup

def check_command(message):
	if message.text == "/start":
		start_message(message)
		return False
	if message.text == "/help":
		show_help(message)
		return False
	if message.text == "/balance":
		show_balance(message)
		return False
	if message.text == "/repeat":
		repeat_prompt(message)
		return False
	return True
    
bot.infinity_polling()


