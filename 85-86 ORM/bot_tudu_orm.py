import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import select, ForeignKey, delete
from typing import List
db_name = 'bot_tudu'
engine = create_engine(f'sqlite:///{db_name}')

token = '7816904868:AAFHft8lEueKEfvVQmNxaEfcIJ3nhhLdxwM'
bot = telebot.TeleBot(token)

ADD_STATE = 'add'
DEL_STATE = 'del'
UP_STATE = 'up'

class TaskModelORM:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')

    def get_tasks(self, user_id):
        with Session(self.engine) as session:
            tasks = session.scalars(select(Task).where(Task.user_id == user_id)).all()
            return tasks
    def get_user(self, telegram_id):
        with Session(self.engine) as session:
            rows = session.scalars(select(User).where(User.telegram_id == telegram_id)).one_or_none()
            return rows

    def add_task(self, addtext, user_id):
        with Session(self.engine) as session:
            task = Task(name=addtext, user_id=user_id, status='выполнить')
            session.add(task)
            session.commit()
    def add_user(self, telegram_id):
        with Session(self.engine) as session:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
    def del_task(self, task_id, user_id):
        with Session(self.engine) as session:
            session.execute(delete(Task).where(Task.user_id == user_id, Task.id == task_id))
            session.commit()

    def up_task(self, task_id, user_id):
        with Session(self.engine) as session:
            task = session.execute(select(Task).where(Task.user_id == user_id, Task.id == task_id)).scalars().one()
            task.status = 'сделано'
            session.commit()

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    status: Mapped[str]
    user: Mapped["User"] = relationship(back_populates='tasks')

    def __repr__(self):
        return f"{self.id} - {self.name}"

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    telegram_id: Mapped[int]
    tasks: Mapped[List["Task"]] = relationship(back_populates='user')

    def __repr__(self):
        return f"{self.telegram_id} - {self.name}"

@bot.message_handler(regexp='привет')
def hello_mes(message):
    bot.reply_to(message, 'привет')

user_state = ''
ADD_STATE = 'add'
db = TaskModelORM('bot_tudu')
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
    print(telegram_id)
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
def del_task(message):
    global user_state
    user_state = UP_STATE
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user.id)
    tasks_str = 'Выбирай задачу: \n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task.name} [{task.status}]\n'
    bot.reply_to(message, tasks_str)

@bot.message_handler(regexp='Удалить задачу')
@bot.message_handler(commands=['del'])
def delete_task(message):
    global user_state
    user_state = DEL_STATE
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user.id)
    tasks_str = 'Выбирай задачу: \n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task.name} \n'
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
    tasks = db.get_tasks(user.id)
    if not tasks:
        return bot.reply_to(message, 'у вас нет задач')
    num_tasks = []
    for number, task in enumerate(tasks, 1):
        num_tasks.append(f'{str(number)}. {task.name} [{task.status}]')
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
        db.add_task(message.text, user.id)
        user_state = ''
        bot.reply_to(message, 'Добавил задачу')
    if user_state == DEL_STATE:
        try:
            task_number = int(message.text)
        except Exception:
            bot.reply_to(message, 'Ошибка')
            return
        user = db.get_user(telegram_id)
        tasks = db.get_tasks(user.id)
        if 0 < task_number < len(tasks)+1:
            task = tasks[task_number-1]
            db.del_task(task.id, user.id)
            bot.reply_to(message, 'Удалил задачу')
        else:
            bot.reply_to(message, 'Нет такой задачи')
    if user_state == UP_STATE:
        try:
            task_number = int(message.text)
        except Exception:
            bot.reply_to(message, 'Ошибка')
            return
        user = db.get_user(telegram_id)
        tasks = db.get_tasks(user.id)
        if 0 < task_number < len(tasks)+1:
            task = tasks[task_number-1]
            db.up_task(task.id, user.id)
            bot.reply_to(message, 'Сделал задачу')
        else:
            bot.reply_to(message, 'Нет такой задачи')

bot.infinity_polling()

