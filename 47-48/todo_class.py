class TaskModel:
    def __init__(self):
        self.tasks = [{'name': 'Поспать', 'status': 'В ожидании'}]
    def get_tasks(self):
        return self.tasks
    def add_task(self, name):
        task = {'name': name, 'status': 'В ожидании'}
        self.tasks.append(task)
    def complete_task(self, task_number):
        self.tasks[task_number]['status'] = "Выполнена"
    def del_task(self, task_number):
        self.tasks.pop(task_number)

class View:
    @staticmethod
    def show_all_tasks(tasks):
        for number, task in enumerate(tasks, 1):
            print(f"{number}. {task['name']}: {task['status']}")
    @staticmethod
    def show_add_task():
        return input('Название задачи: \n>  ')
    @staticmethod
    def show_complete_task():
        return int(input('Введи номер задачи: \n>  '))
    @staticmethod
    def show_del_task():
        return int(input('Введи номер задачи: \n>  '))
class Controler:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    def add_task(self):
        """Добавление задачи"""
        tasks = self.model.get_tasks()
        self.view.show_all_tasks(tasks)
        task_name = self.view.show_add_task()
        self.model.add_task(task_name)
        self.view.show_all_tasks(tasks)
    def chow_tasks(self):
        tasks = self.model.get_tasks()
        self.view.show_all_tasks(tasks)
    def complete_task(self):
        task_number = self.view.show_complete_task()
        task_number -= 1
        self.model.complete_task(task_number)
    def del_task(self):
        task_number = self.view.show_del_task()
        task_number -= 1
        self.model.del_task(task_number)
model = TaskModel()
view = View()
contr = Controler(view, model)

while True:
    print("-МЕНЮ-")
    print("1-Добавить задачу")
    print("2-Выполнить задачу")
    print("3-Посмотреть список задач")
    print("4-Удалить задачу")
    print("5-Выйти")
    print("----")
    choice = input('Что ты хочешь сделать: \n> ')
    if choice == '1':
        contr.add_task()
    elif choice == '2':
        contr.complete_task()
    elif choice == '3':
        print('Задачи')
        contr.chow_tasks()
        print(model.tasks)
    elif choice == '4':
        contr.del_task()
    elif choice == '5':
        break