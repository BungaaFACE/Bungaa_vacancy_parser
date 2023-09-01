class Vacancy:
    # Используем set для избежания повтора вакансий
    all_vacancies = []
    # Для легкого поиска вакансий по id
    id_num = 1

    def __init__(self, title, salary_from, salary_to, currency, town, experience, info, firm_name, url, platform):
        self.id = Vacancy.id_num
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.town = town
        self.experience = experience
        self.info = info
        self.firm_name = firm_name
        self.url = url
        self.platform = platform

        Vacancy.id_num += 1
        Vacancy.all_vacancies.append(self)

    @classmethod
    def clear_vacancies(cls):
        cls.all_vacancies.clear()
        cls.id_num = 1

    def __ge__(self, other):
        # проверка other на принадлежность к int выполнена в Saver
        if self.salary_from:
            return self.salary_from >= other
        elif self.salary_to:
            return self.salary_to >= other
