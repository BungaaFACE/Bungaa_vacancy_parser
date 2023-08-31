from abc import ABC, abstractmethod
from utils import Vacancy
import requests
import json
import os
import re


class Platform(ABC):
    vacancy_class = Vacancy

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def transform_to_instance(self, vacancy_list):
        pass

    def get_api_data(self, platform):
        """returns credential data for platform"""
        credentials_folder = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        credentials_path = os.path.join(credentials_folder, 'credentials.json')

        with open(credentials_path) as credentials_file:
            json_data = json.load(credentials_file)

        return json_data[platform]

    def get_page_data(self, url, params={}, headers={}, retry_num=5):

        for _ in range(retry_num):
            req = requests.get(url, headers=headers, params=params)
            if req.status_code == 200:
                data = req.json()
                req.close()
                return data
            else:
                print(
                    f"Request on page failed with status code: {req.status_code}. Trying again")
                continue
        else:
            print(f'Request failed for {retry_num} times. Abandon.')

    def remove_html_tags(self, text):
        '''remove html <tags> from string'''
        return re.compile(r'<[^>]+>').sub('', text)
