from utils.Saver import Saver
import pandas as pd
import os


XLSX_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.path.sep + 'vacansies.xlsx'


class XLSXSaver(Saver):
    def __init__(self):
        super().__init__()

    def save_to_file(self):
        vacancies_data = [
            vacancy.__dict__ for vacancy in self.vacancies_buffer]

        vacancies_dataframe = pd.DataFrame.from_dict(vacancies_data)
        vacancies_dataframe.to_excel(
            XLSX_PATH, index=False, sheet_name='Vacansies')

        del vacancies_data
        del vacancies_dataframe

    def load_from_file(self):
        self.vacancy_class.clear_vacancies()

        vacancies_dataframe = pd.read_excel(XLSX_PATH, sheet_name='Vacansies')
        vacancies_list = vacancies_dataframe.to_dict("records")

        for vacancy in vacancies_list:
            del vacancy['id']
            self.convert_salary_to_int(vacancy)
            self.vacancy_class(**vacancy)

        del vacancies_dataframe
        del vacancies_list
        super().load_from_file()
