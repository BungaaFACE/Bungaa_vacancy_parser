import os
import requests
from platforms.Platform import Platform


class SuperJobAPI(Platform):
    def __init__(self):
        self.api_key = os.environ['HEADHUNTER_API_KEY']
        self.base_url = os.environ['HEADHUNTER_API_URL']
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def get_vacancies(self, filter_value):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        params = {'keyword': filter_value}

        req = requests.get(url, params=params)
        data = req.json()
        req.close()


if __name__ == '__main__':
    pass
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
