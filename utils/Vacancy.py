class Vacancy:
    all_vacancies = []

    def __init__(self, title, salary_from, salary_to, currency, town, experience, info, firm_name, url, platform):
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
        Vacancy.all_vacancies.append(self)
