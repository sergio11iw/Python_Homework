import telebot
from telebot import types
from sqlalchemy import create_engine, text
db_name = 'bot_tudu'
token = ''
bot = telebot.TeleBot(token)
db_name = 'bot_tudu'
ADD_STATE = 'add'
DEL_STATE = 'del'
UP_STATE = 'up'

class TaskModelSQLAlchemy:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
    def get_tasks(self, user_id):
        with self.engine.connect() as con:
            rows = con.execute(text('select * from task where user_id=:user_id'), {'user_id': user_id}).mappings().all()
            return rows
            print(rows)
    def add_task(self, addtext, user_id):
        with self.engine.connect() as con:
            rows = con.execute(text('insert into task (name, user_id, status) values(:name, :user_id, "выполнить")'), {'user_id': user_id, 'name': addtext})
            con.commit()
            return rows
        print(rows)
    def get_user(self, telegram_id):
        with self.engine.connect() as con:
            rows = con.execute(text('select * from user where telegram_id =:telegram_id'),
                               {'telegram_id': telegram_id}).mappings().one_or_none()
            return rows
            print(rows)
    def add_user(self, telegram_id):
        with self.engine.connect() as con:
            con.execute(text('insert into user (telegram_id) values(:telegram_id)'), {'telegram_id': telegram_id})
            con.commit()
    def del_task(self, task_id, user_id):
        with self.engine.connect() as con:
            con.execute(text('DELETE FROM task WHERE id=:task_id and user_id=:user_id'), {'task_id': task_id, 'user_id': user_id})
            con.commit()
    def up_task(self, task_id, user_id):
        with self.engine.connect() as con:
            con.execute(text("update task set status='сделано' WHERE id=:task_id and user_id=:user_id"), {'task_id': task_id, 'user_id': user_id})
            con.commit()

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

@bot.message_handler(regexp='привет')
def hello_mes(message):
    bot.reply_to(message, 'привет')


db = TaskModelSQLAlchemy('bot_tudu')
@bot.message_handler(commands=['start'])
def start(message):
    description = 'Я бот, жми кнопку'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Список задач')
    button2 = types.KeyboardButton('Добавить задачу')
    button3 = types.KeyboardButton('Удалить задачу')
    button4 = types.KeyboardButton('Изменить статус задачи')
    markup.add(button1)
    markup.row(button2, button3, button4)
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

@bot.message_handler(regexp='Изменить статус задачи')
@bot.message_handler(commands=['up'])
def delete(message):
    global user_state
    user_state = UP_STATE
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user['id'])
    tasks_str = 'Выбирай задачу: \n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task["name"]} [{task["status"]}]\n'
    bot.reply_to(message, tasks_str)
@bot.message_handler(regexp='Удалить задачу')
@bot.message_handler(commands=['del'])
def delete(message):
    global user_state
    user_state = DEL_STATE
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user['id'])
    tasks_str = 'Выбирай задачу: \n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task["name"]} [{task["status"]}]\n'
    bot.reply_to(message, tasks_str)

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
    num_tasks = []
    for number, task in enumerate(tasks, 1):
        num_tasks.append(f'{str(number)}. {task["name"]} [{task["status"]}]')
    tasks_string = '\n' .join(num_tasks)
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
    if user_state == DEL_STATE:
        try:
            task_number = int(message.text)
        except Exception:
            #print('error')
            bot.reply_to(message, 'Ошибка')
            return
        user = db.get_user(telegram_id)
        tasks = db.get_tasks(user['id'])
        if 0 < task_number < len(tasks)+1:
            task = tasks[task_number-1]
            #print(task)
            db.del_task(task['id'], user['id'])
            bot.reply_to(message, 'Удалил задачу')
        else:
            #print('NO ZAD')
            bot.reply_to(message, 'Нет такой задачи')
    if user_state == UP_STATE:
        try:
            task_number = int(message.text)
        except Exception:
            #print('error')
            bot.reply_to(message, 'Ошибка')
            return
        user = db.get_user(telegram_id)
        tasks = db.get_tasks(user['id'])
        if 0 < task_number < len(tasks)+1:
            task = tasks[task_number-1]
            #print(task)
            db.up_task(task['id'], user['id'])
            bot.reply_to(message, 'Сделал задачу')
        else:
            #print('NO ZAD')
            bot.reply_to(message, 'Нет такой задачи')
bot.infinity_polling()

