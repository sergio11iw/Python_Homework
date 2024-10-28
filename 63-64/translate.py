import requests

class YandexTranslate:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog

    def send_request(self, text, target):
        payload = {
            "sourceLanguageCode": "ru",
            "targetLanguageCode": f"{target}",
            "format": "HTML",
            "texts": [
                f"{text}"],
            "folderId": f"{self.catalog}",
            "speller": False
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }
        url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
        response = requests.post(url, json=payload, headers=headers)
        text = response.json()['translations'][0]['text']
        print(text)
        return text




