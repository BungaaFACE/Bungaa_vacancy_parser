import os
import sys
import requests
from platforms.Platform import Platform
from utils import VacanciesNotAvailable


class HeadHunterAPI(Platform):
    def __init__(self):
        # self.api_key = os.environ['HEADHUNTER_API_KEY']
        # self.base_url = os.environ['HEADHUNTER_API_URL']
        # self.user_agent = os.environ['HEADHUNTER_USER_AGENT']
        # self.headers = {'Authorization': f'Bearer {self.api_key}'}
        pass

    def transform_to_instance(self, vacancy_list):
        # title, salary_from, salary_to, currency, town, experience, info, firm_name, url, platform
        for vacancy in vacancy_list:
            title = vacancy['name']
            if vacancy.get('salary'):
                salary_from = vacancy['salary'].get('from', '')
                salary_to = vacancy['salary'].get('to', '')
                currency = vacancy['salary'].get('currency', '')
            else:
                salary_from = 'Не указана'
                salary_to = ''
                currency = ''
            if currency == 'RUR':
                currency = 'rub'
            town = vacancy['area'].get('name', 'Не указан')
            experience = vacancy['experience'].get('name', 'Не указан')

            requirement = self.remove_html_tags(
                vacancy['snippet'].get('requirement', '') or '')
            responsibility = self.remove_html_tags(
                vacancy['snippet'].get('responsibility', '') or '')

            if requirement and responsibility:
                info = f'Требования: {requirement} Ответственность: {responsibility}'
            elif not requirement and not responsibility:
                info = 'Не указана'
            else:
                info = requirement + responsibility
            firm_name = vacancy['employer'].get('name', 'Не указано')
            url = vacancy.get('alternate_url', 'Отсутствует')
            platform = 'HeadHunter'

            self.vacancy_class(title, salary_from, salary_to, currency,
                               town, experience, info, firm_name, url, platform)

    def get_vacancies(self, filter_value=''):
        url = "https://api.hh.ru/vacancies"
        params = {
            "area": 1,  # Specify the desired area ID (1 is Moscow)
            "page": 0,  # Specify the page number
            "per_page": 100,  # Number of vacancies per page
            "host": 'hh.ru'
        }
        # Если ищем по ключевым словам
        if filter_value:
            params['text'] = filter_value

        per_page = 100
        fault_get = 0
        while True:

            page_data = self.get_page_data(url, params=params)

            if page_data:
                page_vacancies = page_data['items']
                self.transform_to_instance(page_vacancies)
                params['page'] += 1
                fault_get = 0

                # Если вакансий на странице меньше максимального, эта страница последняя
                if len(page_vacancies) < per_page:
                    break

            # Если данных нет и страница нулевая - то прекращаем поиск
            elif params['page'] == 0:
                raise VacanciesNotAvailable(
                    'Список вакансий HeadHunter недоступен. Попробуйте позже')

            else:
                fault_get += 1
                params['page'] += 1
                # Если 3 страницы подряд не грузятся - останавливаем загрузку
                if fault_get == 3:
                    print(
                        f'HH API не дает выгрузить страницы после {params["page"]-3}. Остановка.')
                    break


if __name__ == '__main__':
    sys.path.insert(0,
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    hh_api = HeadHunterAPI()
    hh_api.get_vacancies('Python Developer')
    print(hh_api.vacancy_class.all_vacancies)

''' vacancy {
    'id': '73078936', 
    'premium': False, 
    'name': 'Cпециалист контактного центра (лид-менеджер), удаленно', 
    'department': None, 
    'has_test': False, 
    'response_letter_required': False, 
    'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1?host=hh.ru'}, 
    'salary': {'from': 30000, 'to': 60000, 'currency': 'RUR', 'gross': False}, 
    'type': {'id': 'open', 'name': 'Открытая'}, 
    'address': None, 
    'response_url': None, 
    'sort_point_distance': None, 
    'published_at': '2023-08-29T14:31:49+0300', 
    'created_at': '2023-08-29T14:31:49+0300', 
    'archived': False, 
    'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=73078936', 
    'show_logo_in_search': None, 
    'insider_interview': None, 
    'url': 'https://api.hh.ru/vacancies/73078936?host=hh.ru', 
    'alternate_url': 'https://hh.ru/vacancy/73078936', 
    'relations': [], 
    'employer': {'id': '2515303', 
        'name': 'AFISHA AGENCY', 
        'url': 'https://api.hh.ru/employers/2515303?host=hh.ru', 
        'alternate_url': 'https://hh.ru/employer/2515303', 
        'logo_urls': {
            'original': 'https://hhcdn.ru/employer-logo-original/897506.jpg', 
            '90': 'https://hhcdn.ru/employer-logo/4030711.jpeg', 
            '240': 'https://hhcdn.ru/employer-logo/4030712.jpeg'}, 
        'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=2515303&host=hh.ru', 
        'accredited_it_employer': False, 
        'trusted': True}, 
    'snippet': {
        'requirement': 'Гарнитура или наушники + микрофон. ◾️ Стабильное интернет соединение. ◾️ Google Chrome последняя версия. ◾️ С грамотной речью. ◾️ Уверенный пользователь ПК с быстрой...', 
        'responsibility': 'цикл выявления лида 3,5 минуты! ◾️ Работать за компьютером (ноутбуком) и совершать звонки по ip-телефонии. ◾️ Проводить опрос по скрипту...'}, 
    'contacts': None, 
    'schedule': None, 
    'working_days': [], 
    'working_time_intervals': [], 
    'working_time_modes': [], 
    'accept_temporary': True, 
    'professional_roles': [{'id': '83', 'name': 'Оператор call-центра, специалист контактного центра'}], 
    'accept_incomplete_resumes': True, 
    'experience': {
        'id': 'noExperience', 
        'name': 'Нет опыта'}, 
    'employment': {
        'id': 'full', 
        'name': 'Полная занятость'}, 
    'adv_response_url': None, 
    'is_adv_vacancy': False}
    }'''
