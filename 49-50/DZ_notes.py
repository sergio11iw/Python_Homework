import tkinter as tk
from  abc import ABC, abstractmethod
class NoteModel:

    def __init__(self):
        self._notes = [{'id': 1, 'text': 'сижу'}]

    def get_notes(self):
        return self._notes
    def add_note(self, text):
        if len(self._notes) == 0:
            next_id = 1
            note = {'id': next_id, 'text': text}
            self._notes.append(note)
        else:
            next_id = self._get_last_id() + 1
            note = {'id': next_id, 'text': text}
            self._notes.append(note)

    def del_note(self, num):
        if 0 < num <= len(self._notes):
            self._notes.pop(num-1)
            print('Заметка уничтожена')
            notes = []
            count = 0
            for el in self._notes:
                count += 1
                el['id'] = count
                notes.append(el)
            self._notes = notes
        else:
            print('Заметки с таким номером не существует')

    def _get_last_id(self):
        max = self._notes[0]['id']
        for note in self._notes:
            if note['id'] > max:
                max = note['id']
        return max

class AbstractView(ABC):
    @abstractmethod
    def render_notes(self, notes):
        pass

class GraphView(AbstractView):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Заметки')
        self.listbox = tk.Listbox(self.root, height=10, width=50)
        self.listbox.pack(padx=10, pady=10)

    def render_notes(self, notes):
        for note in notes:
            text = f"{note['id']} --- {note['text']}"
            self.listbox.insert(tk.END, text)
        self.root.mainloop()
class ConsoleView(AbstractView):
    def render_notes(self, notes):
        if len(notes) == 0:
            print('Все заметки уничтожены')
        else:
            for note in notes:
                text = f"{note['id']} --- {note['text']}"
                print(text)

class Controllet:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_notes(self):
        notes = self.model.get_notes()
        self.view.render_notes(notes)
        # for note in notes:
        #     print(f"{note['id']} - {note['text']}")

    def add_note(self):
        text = input('введите текст заметки\n> ')
        self.model.add_note(text)

    def del_note(self):
        num = int(input('введите номер заметки\n> '))
        self.model.del_note(num)


model = NoteModel()
graphview = GraphView()
consoleview = ConsoleView()
contr = Controllet(model, consoleview)

while True:
    print('\n\n1 - Посмотреть все заметки')
    print('2 - Добавить заметку')
    print('3 - Удалить заметку')
    print('4 - Выйти')

    chouce = input('выбирай:\n> ')

    if chouce == '1':
        contr.show_notes()
    elif chouce == '2':
        contr.add_note()
    elif chouce == '3':
        contr.del_note()
    elif chouce == '4':
        break