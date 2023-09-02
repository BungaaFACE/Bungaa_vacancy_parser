from utils.Saver import Saver
import json
import os


TXT_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.path.sep + 'vacancies.txt'


class TXTSaver(Saver):
    def __init__(self):
        self.vacancy_sep = f'\n{"=" * 30}\n'
        super().__init__()

    def save_to_file(self):
        vacancies_data = [str(vacancy.__dict__)[1:-1]
                          for vacancy in self.vacancies_buffer]

        vacancies_str = self.vacancy_sep.join(
            vacancies_data).replace(", '", "\n'").replace("'", "")

        with open(TXT_PATH, 'w', encoding='utf-8') as txt_file:
            txt_file.write(vacancies_str)

        del vacancies_data
        del vacancies_str

    def load_from_file(self):
        self.vacancy_class.clear_vacancies()

        with open(TXT_PATH, 'r', encoding='utf-8') as txt_file:
            vacancies_str = txt_file.read()

        for vacancy in vacancies_str.split(self.vacancy_sep):
            vacancy_dict = {}
            for parameter in vacancy.split('\n'):
                splitted_data = parameter.split(': ')
                key = splitted_data[0]
                value = ': '.join(splitted_data[1:])

                if key != 'id':
                    vacancy_dict[key] = value

            self.convert_salary_to_int(vacancy_dict)
            self.vacancy_class(**vacancy_dict)

        del vacancies_str
        super().load_from_file()
