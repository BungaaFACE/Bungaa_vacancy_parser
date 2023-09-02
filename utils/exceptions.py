class VacanciesNotAvailable(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotImplementedPlatforms(Exception):
    def __init__(self, message):
        super().__init__(message)
