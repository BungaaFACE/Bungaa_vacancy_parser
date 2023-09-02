import os
import requests
if __name__ != '__main__':
    from platforms.Platform import Platform
    from utils import VacanciesNotAvailable
else:
    from Platform import Platform


class SuperJobAPI(Platform):
    def __init__(self):
        credentials = self.get_api_data('SuperJob')
        id = int(credentials['app_id'])
        user_login = credentials['login']
        user_password = credentials['password']
        self.secret = credentials['app_secret']
        url = 'https://api.superjob.ru/2.0/oauth2/password/'
        headers = {
            'login': user_login,
            'password': user_password,
            'client_id': id,
            "client_secret": self.secret}
        req = requests.get(url, params=headers)
        self.access_token = req.json()['access_token']
        self.token_type = req.json()['token_type']
        self.authorization = f'{self.token_type} {self.access_token[3:]}'
        self.headers = {'Host': 'api.superjob.ru',
                        'X-Api-App-Id': self.secret,
                        'Authorization': self.authorization,
                        'Content-Type': 'application/json', }

    def transform_to_instance(self, vacancy_list):
        # title, salary_from, salary_to, currency, town, experience, info, firm_name, url, platform
        for vacancy in vacancy_list:
            title = vacancy['profession']
            salary_from = vacancy.get('payment_from', '')
            salary_to = vacancy.get('payment_to', '')
            currency = vacancy.get('currency', '')
            town = vacancy['town'].get('title', '')
            experience = vacancy['experience'].get('title', '')
            info = self.remove_html_tags(vacancy.get('vacancyRichText') or '')
            firm_name = vacancy.get('firm_name', '')
            url = vacancy.get('link', '')
            platform = 'SuperJob'

            self.vacancy_class(title, salary_from, salary_to, currency,
                               town, experience, info, firm_name, url, platform)

    def get_vacancies(self, filter_value=''):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        params = {'count': 100,
                  'page': 0, }
        if filter_value:
            params['keyword'] = filter_value

        per_page = 100
        while True:

            page_data = self.get_page_data(
                url, params=params, headers=self.headers)

            if page_data:
                page_vacancies = page_data['objects']
                self.transform_to_instance(page_vacancies)
                params['page'] += 1

                # Если вакансий на странице меньше максимального, эта страница последняя
                if len(page_vacancies) < per_page:
                    break

            # Если данных нет и страница нулевая - то прекращаем поиск
            elif params['page'] == 0:
                raise VacanciesNotAvailable(
                    'Список вакансий HeadHunter недоступен. Попробуйте позже')

        # Синхронизация найденных вакасний в класс Saver
        super().get_vacancies()


if __name__ == '__main__':
    data = SuperJobAPI().get_vacancies('Python Developer')
    print(data.all)
"""
{
    "objects":[
    {
        "id": 25746005,
        "id_client": 544932,
        "payment_from": 0,
        "payment_to": 0,
        "date_pub_to": 1371640666,
        "date_archived": 1371640666,
        "date_published": 1371554266,
        "address": null,
        "payment": null,
        "profession": "Специалист по согласованиям",
        "work": "1. Подготовка, согласование с Комитетами и службами...",
        "metro": [
            {
                "id": 229,
                "title": "Сенная площадь",
                "id_metro_line": 2
            },
            {
                "id": 230,
                "title": "Невский Проспект",
                "id_metro_line": 2
            },
            {
                "id": 538,
                "title": "Адмиралтейская",
                "id_metro_line": 5
            }
        ],
        "currency": "rub",
        "moveable": true,
        "agreement": true,
        "anonymous": false,
        "type_of_work": {
            "id": 6,
            "title": "Полный рабочий день"
        },
        "place_of_work": {
            "id": 1,
            "title": "на территории работодателя"
        },
        "education": {
            "id": 2,
            "title": "Высшее"
        },
        "experience": {
            "id": 3,
            "title": "от 3 лет"
        },
        "maritalstatus": {
            "id": 0,
            "title": "не имеет значения"
        },
        "children": {
            "id": 0,
            "title": "не имеет значения"
        },
        "already_sent_on_vacancy": false,
        "languages": [],
        "driving_licence": [],
        "catalogues":[
            {
                "id":438,
                "title":"Продажи",
                "positions":[
                    {
                        "id":441,
                        "title":"Бытовая техника, электроника, фото, видео"
                    },
                    { // ... }
                ]
            }
        ],
        "agency": {
            "id": 1,
            "title": "Прямой работодатель"
        },
        "town": {
            "id": 14,
            "title": "Санкт-Петербург",
            "declension": "в Санкт-Петербурге",
            "genitive": "Санкт-Петербурга"
        },
        "client_logo": "https://public.superjob.ru/images/clients_logos.ru/544932.gif",
        "age_from": 35,
        "age_to": 45,
        "gender": {
            "id": 3,
            "title": "женский"
        },
        "firm_name": "Комплекс Галерная 5",
        "firm_activity": "ООО «Комплекс Галерная 5» – дочернее общество...",
        "link": "https://www.superjob.ru/vakansii/specialist-po-soglasovaniyam-25746005-130520.html"
    }
    ],
    "total": 1000000,
    "corrected_keyword": "учитель", // Ключ с исправленным словом возвращается
                                    // только в случае ошибки в исходном ключевом слове
    "more":false
}
"""
