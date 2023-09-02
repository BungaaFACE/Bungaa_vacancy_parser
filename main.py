import export_project_folder
from platforms import HeadHunterAPI, SuperJobAPI
from utils import JSONSaver, TXTSaver, CSVSaver, XLSXSaver, Saver
from utils.exceptions import NotImplementedPlatforms

PLATFORMS = {'1': HeadHunterAPI, '2': SuperJobAPI}
SAVER_FORMATS = {'1': JSONSaver, '2': XLSXSaver, '3': CSVSaver, '4': TXTSaver}
STRING_MENU = """
~~~~~~~~~~~~~~~~MENU~~~~~~~~~~~~~~~~
1: Ввести поисковый запрос
2: Фильтрация ваканский по зарплате
3: Удаление вакансии по ID
4: Сохранить список вакансий в файл
5: Загрузить список вакансий из файла
6: Вывести список вакансий в консоль
7: Изменить платформы для поиска
8: Изменить формат сохранения
0: Выход
~~~~~~~~~~~~~~~~MENU~~~~~~~~~~~~~~~~
"""


class MainStarter:
    def __init__(self) -> None:
        self.platform_list = []
        self.saver_format = None
        self.functions_menu = {'1': self.search_vacancies,
                               '2': self.filter_vacancies_by_salary,
                               '3': self.delete_vacancy_by_id,
                               '4': self.save_to_file,
                               '5': self.load_from_file,
                               '6': self.print_to_console,
                               '7': self.activate_apis,
                               '8': self.activate_saver,
                               '0': self.exit_programm}
        self.main_menu()

    def check_for_emptyness(self):
        if not Saver.vacancies_buffer:
            print('Список вакансий пуст.\n'
                  'Сначала выполните поисковый запрос или загрузите список вакансий из файла')
            return True

    def activate_apis(self):
        platforms_choice = input('Выберите одну или несколько платформ для поиска вакансий:\n'
                                 '    1: HeadHunter\n'
                                 '    2: SuperJob\n'
                                 '    3: Выход в меню\n'
                                 '    По умолчанию выбраны все платформы.\n').strip().lower()
        if platforms_choice == '3':
            return

        elif not platforms_choice:
            platforms_choice = '12'

        for single_choice in platforms_choice:
            if single_choice.isdigit() and single_choice in PLATFORMS.keys():
                self.platform_list.append(PLATFORMS[single_choice]())

        if not self.platform_list:
            raise NotImplementedPlatforms(
                'Платформы с указанными индексами не найдены')

    def search_vacancies(self):
        if not self.platform_list:
            self.activate_apis()
            # Если платформа не назначена, значит пользователь вышел в меню
            if not self.platform_list:
                return

        search_value = input('Введите поисковый запрос:\n'
                             'По умолчанию - получение вакансий без фильтра.\n')

        for platform in self.platform_list:
            platform.get_vacancies(search_value)

    def filter_vacancies_by_salary(self):

        # Если список загруженных вакансий пуст
        if self.check_for_emptyness():
            return

        salary_filter_value = input(
            'Введите минимальный порог зарплаты:\n').lower().strip()

        while True:
            if salary_filter_value == 'exit':
                return
            try:
                salary_filter_value = int(salary_filter_value)
                Saver.get_vacancies_by_salary(salary_filter_value)
                return
            except ValueError:
                salary_filter_value = input(
                    'Вы ввели некорректный формат.\nПопроуйте снова или введите \'exit\' для выхода в меню:\n').lower().strip()

    def delete_vacancy_by_id(self):

        # Если список загруженных вакансий пуст
        if self.check_for_emptyness():
            return

        deletion_id = input(
            'Введите id вакансии для удаления или \'exit\' для выхода в меню:\n').lower().strip()
        while True:
            if deletion_id == 'exit':
                return
            try:
                deletion_id = int(deletion_id)
                Saver.delete_vacancy_by_id(deletion_id)
                return
            except ValueError as e:
                # raise e
                deletion_id = input(
                    'Вы ввели некорректный формат.\nПопроуйте снова или введите \'exit\' для выхода в меню:\n').lower().strip()

    def activate_saver(self):
        while True:
            saver_choice = input('Выберите формат для сохранения вакансий:\n'
                                 '    1: JSON\n'
                                 '    2: XLSX\n'
                                 '    3: CSV\n'
                                 '    4: TXT\n'
                                 '    5: Выход в меню\n'
                                 '    По умолчанию: JSON\n').strip().lower()

            if saver_choice == '5':
                return
            if not saver_choice:
                saver_choice = '1'

            if saver_choice.isdigit() and saver_choice in SAVER_FORMATS.keys():
                self.saver_format = SAVER_FORMATS[saver_choice]()
                break

            else:
                print('Формат не найден. Попробуйте снова.')

    def save_to_file(self):
        # Если список загруженных вакансий пуст
        if self.check_for_emptyness():
            return

        if not self.saver_format:
            self.activate_saver()
            # Если формат не назначен, значит пользователь вышел в меню
            if not self.saver_format:
                return

        self.saver_format.save_to_file()

    def load_from_file(self):
        if not self.saver_format:
            self.activate_saver()
            # Если формат не назначен, значит пользователь вышел в меню
            if not self.saver_format:
                return

        self.saver_format.load_from_file()

    def print_to_console(self):
        # Если список загруженных вакансий пуст
        if self.check_for_emptyness():
            return

        Saver.print_to_console()

    def exit_programm(self):
        print('Спасибо за использование программы!')
        exit()

    def main_menu(self):
        while True:
            user_choice = input(STRING_MENU).strip().lower()

            if self.functions_menu.get(user_choice):
                self.functions_menu[user_choice]()
            else:
                print('Указан несуществующий пункт меню.\n')


if __name__ == "__main__":
    MainStarter()
