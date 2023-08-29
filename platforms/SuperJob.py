import os
from platforms.Platform import Platform


class SuperJobAPI(Platform):
    def __init__(self):
        self.api_key = os.environ['HEADHUNTER_API_KEY']
        self.base_url = os.environ['HEADHUNTER_API_URL']
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def get_vacancies(self):
        pass
