import telebot
from telebot import types
from translate import YandexTranslate


token = '-'
bot = telebot.TeleBot(token)

user_state = ''
TRANS_STATE = 'trans'
target = 'en'


y_token = '-'
y_catalog = '-'

yandex_bot = YandexTranslate(y_token, y_catalog)


@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот - переводчик. Жми на кнопку или вводи команду /trans перевести текст'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Перевести текст')
    button2 = types.KeyboardButton('Сменить язык')
    button3 = types.KeyboardButton('Завершить перевод')
    markup.add(button)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, description, reply_markup=markup)

@bot.message_handler(regexp='Завершить перевод')
@bot.message_handler(commands=['end'])
def end_state(message):
    global user_state
    user_state = ''
    bot.reply_to(message, "Переводчик отключен")

@bot.message_handler(commands=["lang"])
@bot.message_handler(regexp='Сменить язык')
def lag(message):
    global user_state
    user_state = 'lang'
    bot.reply_to(message, 'Сменить язык')

@bot.message_handler(commands=["trans"])
@bot.message_handler(regexp='Перевести текст')
def trans(message):
    global user_state
    user_state = TRANS_STATE
    bot.reply_to(message, 'Перевод начат. Чтобы выйти - жми команду /end или кнопку')

@bot.message_handler(func=lambda message: True)
def get_question(message):
    global target
    global user_state
    if user_state == TRANS_STATE:
        response = yandex_bot.send_request(message.text, target)
        bot.reply_to(message, response)
    elif user_state == 'lang':
        target = message.text
        bot.reply_to(message, f'Сменил язык на {target}')

bot.infinity_polling()