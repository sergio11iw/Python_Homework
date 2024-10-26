import telebot
import random
from telebot import types
token = ''

bot = telebot.TeleBot(token)

user_state = ''
ADD_STATE = 'game'

@bot.message_handler(commands=['start'])
def start(message):
    description = 'Я бот, жми кнопку играть'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Играть')
    markup.add(button)
    bot.send_message(message.chat.id, description, reply_markup=markup)

@bot.message_handler(regexp='Играть')
@bot.message_handler(commands=['game'])
def game(message):
    global user_state
    user_state = ADD_STATE
    bot.reply_to(message, 'Введи число от 0 до 1:')

@bot.message_handler(commands=['end'])
def end_state(message):
    global user_state
    user_state = ''
    bot.reply_to(message, "Игра завершена")

@bot.message_handler(func=lambda message: True)
def get_task(message):
    global user_state
    res = random.randint(0, 1)
    if user_state == ADD_STATE:
        if message.text == str(res):
            bot.reply_to(message, 'Угадал. Игра завершена')
            user_state = ''
        else:
            bot.reply_to(message, 'Не угадал, продолжаем. /end - выход')

bot.infinity_polling()

