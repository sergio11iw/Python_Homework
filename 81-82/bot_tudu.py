import telebot
from telebot import types
import json
import sqlite3 as sq

token = '7474657107:AAE-AdnvCFdDDUABNjmG1psf6VbQAcRGa-U'
bot = telebot.TeleBot(token)
db_name = 'bot_tudu'
ADD_STATE = 'add'

class TaskModelSQL:
    def __init__(self, db_name):
        self.db_name = db_name
        # self.connection = sq.connect(self.db_name)
        # self.connection.row_factory = self._dict_factory
    def get_tasks(self, user_id):
        connection = sq.connect(self.db_name)
        connection.row_factory = self._dict_factory
        cursor = connection.cursor()
        rows = cursor.execute('select * from task where user_id = ?', (user_id, )).fetchall()
        connection.close()
        return rows
    def add_task(self, text, user_id):
        connection = sq.connect(self.db_name)
        connection.row_factory = self._dict_factory
        cursor = connection.cursor()
        cursor.execute('''insert into task (name, user_id) values (?, ?);''', (text, user_id))
        connection.commit()
        connection.close()
    def get_user(self, telegram_id):
        connection = sq.connect(self.db_name)
        connection.row_factory = self._dict_factory
        cursor = connection.cursor()
        rows = cursor.execute('select * from user where telegram_id = ?', (telegram_id, )).fetchone()
        connection.close()
        return rows
    def add_user(self, telegram_id):
        connection = sq.connect(self.db_name)
        connection.row_factory = self._dict_factory
        cursor = connection.cursor()
        cursor.execute('insert into user (telegram_id) values (?)', (telegram_id, ))
        connection.commit()
        connection.close()
    def del_task(self, text, user_id):
        connection = sq.connect(self.db_name)
        connection.row_factory = self._dict_factory
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Task WHERE id = ? and user_id = ?;', (text, user_id))
        connection.commit()
        connection.close()

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class TaskModal:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self._load_from_file()

    def get_tasks(self):
        return self.tasks

    def _load_from_file(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks

    def add_task(self, task):
        self.tasks.append(task)
        self._save_to_file()

    def _save_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f)


@bot.message_handler(regexp='привет')
def hello_mes(message):
    bot.reply_to(message, 'привет')

user_state = ''
ADD_STATE = 'add'
# db = TaskModal('tasks.json')
db = TaskModelSQL('bot_tudu')
@bot.message_handler(commands=['start'])
def start(message):
    description = 'Я бот, жми кнопку'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Добавить задачу')
    button2 = types.KeyboardButton('Список задач')
    button3 = types.KeyboardButton('Удалить задачу по id')
    markup.add(button)
    markup.add(button2)
    markup.add(button3)
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    print(user)
    if not user:
        db.add_user(telegram_id)
        bot.reply_to(message, 'добавлен')
    bot.send_message(message.chat.id, description, reply_markup=markup)


@bot.message_handler(regexp='Добавить задачу')
@bot.message_handler(commands=['add'])
def add(message):
    global user_state
    user_state = ADD_STATE
    bot.reply_to(message, 'Введи текст задачи:')

@bot.message_handler(regexp='Удалить задачу по id')
@bot.message_handler(commands=['del'])
def delete(message):
    global user_state
    user_state = 'DEL'
    bot.reply_to(message, 'Введи id задачи:')

@bot.message_handler(commands=['key'])
def keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Добавить задачу')
    markup.add(button)
    bot.send_message(message.chat.id, 'какой то текст', reply_markup=markup)

@bot.message_handler(regexp='Список задач')
@bot.message_handler(commands=['tasks'])
def get_task_list(message):
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        return bot.reply_to(message, 'вас нет в базе')
    tasks = db.get_tasks(user['id'])
    if not tasks:
        return bot.reply_to(message, 'у вас нет задач')
    id_tasks = []
    for task in tasks:
        id_tasks.append(f"({str(task['id'])}) {task['name']}")
    tasks_string = '\n' .join(id_tasks)
    bot.reply_to(message, tasks_string)

@bot.message_handler(commands=['end'])
def end_state(message):
    global user_state
    user_state = ''
    bot.reply_to(message, "Мы закончили добавление задачи")

@bot.message_handler(func=lambda message: True)
def get_task(message):
    global user_state
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if user_state == ADD_STATE:
        db.add_task(message.text, user['id'])
        user_state = ''
        bot.reply_to(message, 'Добавил текст')
    if user_state == 'DEL':
        db.del_task(message.text, user['id'])
        user_state = ''
        bot.reply_to(message, 'Удалил задачу')

bot.infinity_polling()

