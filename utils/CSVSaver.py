from utils.Saver import Saver
import csv
import os


CSV_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.path.sep + 'vacansies.csv'


class CSVSaver(Saver):
    def __init__(self):
        super().__init__()

    def save_to_file(self):
        vacancies_data = [
            vacancy.__dict__ for vacancy in self.vacancies_buffer]

        keys = vacancies_data[0].keys()

        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(vacancies_data)

        del vacancies_data

    def load_from_file(self):
        self.vacancy_class.clear_vacancies()

        with open(CSV_PATH, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            vacancies_list = list(csv_reader)

        for vacancy in vacancies_list:
            del vacancy['id']
            self.convert_salary_to_int(vacancy)
            self.vacancy_class(**vacancy)

        del vacancies_list
        super().load_from_file()
