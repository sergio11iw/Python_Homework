import sqlite3 as sq
class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sq.connect(self.db_name)
    def get_tasks(self, user_id):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute('select * from note WHERE user_id = ?', (user_id, ))
            rows = cursor.fetchall()
            return rows
    def add_task(self, name, raiting, user_id):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute('''insert into note (name, raiting, user_id) values (?, ?, ?);''', (name, raiting, user_id))
    def top_tasks(self, user_id):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute('select * from note WHERE raiting > 3 AND user_id = ?', (user_id, ))
            rows = cursor.fetchall()
            return rows
    def get_user(self, name, password):
        with self.connection as connection:
            cursor = connection.cursor()
            rows = cursor.execute('select * from user where name = ? and pass = ?', (name, password))
            res = rows.fetchone()
            return res
    def __del__(self):
        print('Заканчиваю работу с базой')
        self.connection.close()
class User:
    def __init__(self, name: str, password: str, db: Database):
        self.name = name
        self.password = password
        self.db = db
    def auth(self):
        user = self.db.get_user(self.name, self.password)
        if user:
            return user[0]
        return None

db = Database('notes')
name = input('Введи имя: \n> ')
password = input('Введи пароль: \n> ')
auth = False
user_id = User(name, password, db).auth()
if user_id:
    auth = True
    print('Успех')
else:
    print('Не верный логин или пароль')

while True and auth:
    print('\nЗаметки')
    print("1-Добавить заметку")
    print("2-Читать заметки")
    print("3-Самые популярные заметки")
    print("4-Выйти")
    print()
    choice = input('Что ты хочешь сделать: \n> ')
    if choice == '1':
        name = input("Название задачи: \n> ")
        raiting = 6
        while True:
            raiting = int(input("Рейтинг задачи (от 0 до 5): \n> "))
            if 0 <= raiting <= 5:
                db.add_task(name, raiting, user_id)
                break
    elif choice == '2':
        rows = db.get_tasks(user_id)
        print('\nСписок заметок:')
        for row in rows:
           print(f'{row[0]}. {row[1]} - {row[2]}')
    elif choice == '3':
        rows = db.top_tasks(user_id)
        print('\nСамые популярные заметки:')
        for row in rows:
            print(f'{row[0]}. {row[1]} - {row[2]}')
    elif choice == '4':
        break