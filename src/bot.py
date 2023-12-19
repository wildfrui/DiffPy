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


# roflan comment
def roflanpass():
	pass


roflanpass()


# подумать где хранить длинный текст
@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, "Привет! Я бот, который генерирует картинки по запросу!")
	markup = generate_keyboard_generation()
	bot.send_message(message.chat.id, "Выберите вариант взаимодействия с моделью:", reply_markup=markup)
	# bot.register_next_step_handler(sent_msg, input_prompt)
 
@bot.message_handler(commands=['help'])
def show_help(message):
	bot.send_message(message.chat.id, "Привет! Я могу тебе помочь")
 
@bot.message_handler(commands=['balance'])
def show_balance(message):
	balance = user.get_user_balance()
	bot.send_message(message.chat.id, f"Доступно токенов: {balance}")
 
@bot.message_handler(commands=['translate'])
def translate_text(message):
	balance = user.get_user_balance()
	bot.send_message(message.chat.id, f"Доступно токенов: {balance}")

@bot.message_handler(content_types=['text'])
def input_prompt(message):
	if message.text == "Генерация по тексту":
		sent_msg = bot.send_message(message.chat.id, "Напишите текст, который хотите сгенерировать:", reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(sent_msg, choose_style)

def choose_style(message):
	global pic
	if check_command(message):
		print(message.text)
		pic.set_prompt(message.text)
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
			markup = generate_keyboard_generation()
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

def generate_keyboard_generation():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item = types.KeyboardButton("Генерация по тексту")
	markup.add(item)
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
	return True
    
bot.infinity_polling()


