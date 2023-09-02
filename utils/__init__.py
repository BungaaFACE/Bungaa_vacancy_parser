from utils.exceptions import VacanciesNotAvailable
from utils.Vacancy import Vacancy
from utils.Saver import Saver
from utils.JSONSaver import JSONSaver
from utils.TXTSaver import TXTSaver
from utils.CSVSaver import CSVSaver
from utils.XLSXSaver import XLSXSaver

# Позволяет скопировать результаты поиска из API в класс Saver
sync_vacancies = Saver.sync_vacancy_list
