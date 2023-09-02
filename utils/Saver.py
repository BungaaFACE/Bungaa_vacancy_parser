from abc import ABC, abstractmethod
from utils import Vacancy


class Saver(ABC):
    '''Parent class for manipulating vacancies classes.'''
    vacancies_buffer = []
    vacancy_class = Vacancy

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        Vacancy.all_vacancies = self.vacancies_buffer.copy()

    @classmethod
    def add_vacancy(cls, vacancy):
        cls.vacancies_buffer.append(vacancy)

    @classmethod
    def clear_vacancy_list(cls):
        cls.vacancies_buffer.clear()

    @classmethod
    def sync_vacancy_list(cls):
        cls.vacancies_buffer = Vacancy.all_vacancies.copy()

    @classmethod
    def get_vacancies_by_salary(cls, salary):

        if isinstance(salary, int):
            # Очищаем предыдущий результат
            cls.clear_vacancy_list()
            for vacancy in Vacancy.all_vacancies:
                if vacancy >= salary:
                    cls.add_vacancy(vacancy)
        else:
            raise TypeError(
                f'Зарплата не является числом. Получен {type(salary)}')

    @classmethod
    def delete_vacancy(cls, vacancy):
        if isinstance(vacancy, Vacancy) and vacancy in cls.vacancies_buffer:
            cls.vacancies_buffer.remove(vacancy)
        else:
            print('Этой вакансии нет в списке')

    @classmethod
    def delete_vacancy_by_id(cls, del_id):
        if isinstance(del_id, int):
            for index in range(len(cls.vacancies_buffer)):
                if cls.vacancies_buffer[index].__dict__['id'] == del_id:
                    del cls.vacancies_buffer[index]
                    break
            else:
                print(f'Вакансии с id {del_id} нет в списке')
        else:
            print('Некорректный формат id')

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

    @classmethod
    def print_to_console(cls):
        for vacancy in cls.vacancies_buffer:
            vacancy_dict = vacancy.__dict__.copy()
            print('-' * 40)
            print(f"id - {vacancy_dict['id']}")
            print(f"title - {vacancy_dict['title']}")
            print(f"salary from - {vacancy_dict['salary_from']}")
            print(f"salary to - {vacancy_dict['salary_to']}")
            print(f"currency - {vacancy_dict['currency']}")
            print(f"town - {vacancy_dict['town']}")
            print(f"experience - {vacancy_dict['experience']}")
            print(f"url - {vacancy_dict['url']}")
            print(f"platform - {vacancy_dict['platform']}")
