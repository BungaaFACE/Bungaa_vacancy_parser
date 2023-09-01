from abc import ABC, abstractmethod
from utils import Vacancy


class Saver(ABC):
    '''Parent class for manipulating vacancies classes.'''
    vacancies_buffer = []
    vacancy_class = Vacancy

    def __init__(self):
        # По умолчанию забираем все вакансии
        self.vacancies_buffer = Vacancy.all_vacancies

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        Vacancy.all_vacancies = self.vacancies_buffer

    @classmethod
    def add_vacancy(cls, vacancy):
        cls.vacancies_buffer.append(vacancy)

    @classmethod
    def clear_vacancy_list(cls):
        cls.vacancies_buffer.clear()

    @staticmethod
    def get_vacancies_by_salary(cls, salary):

        if isinstance(salary, int):
            # Очищаем предыдущий результат
            cls.clear_vacancy_list()
            for vacancy in Vacancy.all_vacancies:
                if vacancy > salary:
                    cls.add_vacancy(vacancy)
        else:
            raise TypeError(
                f'Зарплата должна быть типа int, или числом, записанным в str. Получен {type(salary)}')

    @staticmethod
    def delete_vacancy(cls, vacancy):
        if isinstance(vacancy, Vacancy) and vacancy in cls.vacancies_buffer:
            cls.vacancies_buffer.remove(vacancy)
        else:
            print('Этой вакансии нет в списке')

    @staticmethod
    def delete_vacancy_by_id(cls, id):
        if isinstance(id, int):
            for index in range(len(cls.vacancies_buffer)):
                if cls.vacancies_buffer[index]['id'] == id:
                    del cls.vacancies_buffer[index]
                    break
        else:
            print(f'Вакансии с {id} нет в списке')

    @staticmethod
    def convert_salary_to_int(vacancy_dict):
        try:
            vacancy_dict['salary_from'] = int(vacancy_dict['salary_from'])
        except:
            vacancy_dict['salary_from'] = ""

        try:
            vacancy_dict['salary_to'] = int(vacancy_dict['salary_to'])
        except:
            vacancy_dict['salary_to'] = ""
