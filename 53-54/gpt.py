import requests
import tkinter as tk

class NoteWindows:
    def __init__(self, bot):
        self.bot = bot
        self.create_window()
        self.root.mainloop()
    def create_window(self):
        self.root = tk.Tk()
        self.root.title('YandexGPT')
        #ввод
        self.input = tk.Text(self.root, height=10, width=20)
        self.input.grid(row=0, column=0, padx=10, pady=10)
        #вывод
        self.output = tk.Listbox(self.root, height=10, width=150)
        self.output.grid(row=0, column=1, padx=10, pady=10)
        #кнопка
        self.button = tk.Button(self.root, text='Отправить', command=self.add_out)
        self.button.grid(row=1, column=0, padx=10, pady=10)
    def add_out(self):
        text = self.input.get('1.0', tk.END)
        res = self.bot.send_request(text)
        self.output.insert(tk.END, 'Вопрос: 'f'{text}')
        self.output.insert(tk.END, 'Ответ: 'f'{res}')

class YandexGPT:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog
    def send_request(self, question):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = {
            "modelUri": f'gpt://{self.catalog}/yandexgpt-lite',
            'completionOptions': {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Отвечай цитатами из фильмов"
                },
                {
                    "role": "user",
                    "text": f'{question}'
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        text = response.json()['result']['alternatives'][0]['message']['text']
        return text

token = 'AQVN02DysF8im3YO2KQT4qrbr4IRwaoCVVgAYwqe'
catalog = 'b1gtphdg2vndncqf33o7'

bot = YandexGPT(token, catalog)
window = NoteWindows(bot)
