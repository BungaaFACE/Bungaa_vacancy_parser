from utils.Saver import Saver
import json
import os

JSON_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.path.sep + 'vacancies.json'


class JSONSaver(Saver):
    def __init__(self):
        super().__init__()

    def save_to_file(self):
        vacancies_data = [
            vacancy.__dict__ for vacancy in self.vacancies_buffer]

        with open(JSON_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(vacancies_data, json_file,
                      ensure_ascii=False, indent=2)
        del vacancies_data

    def load_from_file(self):
        self.vacancy_class.clear_vacancies()

        with open(JSON_PATH, 'r', encoding='utf-8') as json_file:
            vacancies_json = json.load(json_file)

        for vacancy in vacancies_json:
            del vacancy['id']
            self.convert_salary_to_int(vacancy)
            self.vacancy_class(**vacancy)

        del vacancies_json
        super().load_from_file()
