import os
import sys
import requests
if __name__ != '__main__':
    from platforms.Platform import Platform
    from utils import VacanciesNotAvailable
else:
    from Platform import Platform


class HeadHunterAPI(Platform):
    def __init__(self):
        # self.api_key = os.environ['HEADHUNTER_API_KEY']
        # self.base_url = os.environ['HEADHUNTER_API_URL']
        # self.user_agent = os.environ['HEADHUNTER_USER_AGENT']
        # self.headers = {'Authorization': f'Bearer {self.api_key}'}
        pass

    def parse_vacancy_data(self, vacancy_dict):
        """    'id': '73078936', 
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
                'alternate_url': 'https://hh.ru/vacancy/73078936', """
        if vacancy_dict['type'].get('id') == 'open':
            name = vacancy_dict['name']
            location = vacancy_dict['area']['name']
            salary = f"{vacancy_dict['salary']['from']}-{vacancy_dict['salary']['to']} {vacancy_dict['salary']['currency']}"
            url = vacancy_dict['alternate_url']

    def get_vacancies(self, filter_words=''):
        def get_page_data(filter_words='', page=0, retry_num=5):

            url = "https://api.hh.ru/vacancies"
            params = {
                "area": 1,  # Specify the desired area ID (1 is Moscow)
                "page": page,  # Specify the page number
                "per_page": 100,  # Number of vacancies per page
                "host": 'hh.ru'
            }
            # Если ищем по ключевым словам
            if filter_words:
                params['text'] = filter_words
            # Посылаем запрос к API
            for _ in range(retry_num):
                req = requests.get(url, params)
                if req.status_code == 200:
                    data = req.json()
                    req.close()
                    return data
                else:
                    print(
                        f"Request failed with status code: {req.status_code}. Trying again")
                    continue
            else:
                print(f'Request failed for {retry_num} times. Skipping page.')

        self.all_vacancies = []
        data = get_page_data(filter_words)
        return data
        if data:
            all_vacancies.extend(data["items"])
            # data['pages'] показывает некорректное кол-во страниц, поэтому рассчитываем вручную
            num_of_pages = int(data['found']) // 100 + 1

            for page in range(1, num_of_pages+1):
                data = get_page_data(filter_words, page)

            return self.all_vacancies

        else:
            raise VacanciesNotAvailable(
                'Список вакансий HeadHunter недоступен. Попробуйте позже')


if __name__ == '__main__':
    vacancies = HeadHunterAPI().get_vacancies('Python')
    print(vacancies['items'][0]['snippet']['responsibility'])
    # vacancies{
    # 'items', - вакансии
    # 'found', - количество найденных вакансий
    # 'pages', - кол-во страниц - некорректное кол-во
    # 'per_page' - кол-во страниц}

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
