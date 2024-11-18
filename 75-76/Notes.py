import sqlite3 as sq

def get_tasks():
    connection = sq.connect('notes')
    cursor = connection.cursor()
    cursor.execute('select * from note')
    rows = cursor.fetchall()
    connection.close()
    return rows
def add_task(name, raiting):
    connection = sq.connect('notes')
    cursor = connection.cursor()
    cursor.execute('''insert into note (name, raiting) values (?, ?);''', (name, raiting))
    connection.commit()
    connection.close()
def top_tasks():
    connection = sq.connect('notes')
    cursor = connection.cursor()
    cursor.execute('select * from note WHERE raiting > 3')
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows
while True:
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
                add_task(name, raiting)
                break
    elif choice == '2':
        print('\nСписок заметок:')
        for row in get_tasks():
           print(f'{row[0]}. {row[1]} - {row[2]}')
    elif choice == '3':
        print('\nСамые популярные заметки:')
        for row in top_tasks():
            print(f'{row[0]}. {row[1]} - {row[2]}')
    elif choice == '4':
        break
