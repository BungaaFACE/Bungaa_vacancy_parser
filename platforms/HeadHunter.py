import os
import sys
import requests
if __name__ != '__main__':
    from platforms.Platform import Platform
else:
    from Platform import Platform


class HeadHunterAPI(Platform):
    def __init__(self):
        # self.api_key = os.environ['HEADHUNTER_API_KEY']
        # self.base_url = os.environ['HEADHUNTER_API_URL']
        # self.user_agent = os.environ['HEADHUNTER_USER_AGENT']
        # self.headers = {'Authorization': f'Bearer {self.api_key}'}
        pass

    def get_vacancies(self, filter_words='', page=0):
        url = "https://api.hh.ru/vacancies"
        params = {
            "area": 1,  # Specify the desired area ID (1 is Moscow)
            "page": page,  # Specify the page number
            "per_page": 10,  # Number of vacancies per page
            "host": 'hh.ru'
        }
        if filter_words:
            params['text'] = filter_words
        # headers = {"User-Agent": self.user_agent}
        req = requests.get(url, params)  # Посылаем запрос к API
        # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = req.content.decode()
        req.close()
        return data


if __name__ == '__main__':
    vacancies = HeadHunterAPI().get_vacancies('Python')
    print(vacancies)
