# Bungaa_vacancy_parser
Программа получает информацию о вакансиях с разных платформ в России, сохраняет ее в файл и позволяет удобно работать с ней (добавление, фильтрация, удаление).  
# Платформы для сбора вакансий
1. **hh.ru**  
2. **superjob.ru**
# Взаимодействие с пользователем
Coming soon...
# Реализация  
1. Абстрактный класс для работы с API сайтов с вакансиями. Реализация классов, наследующихся от абстрактного класса, для работы с конкретными платформами.  
2. Класс для работы с вакансиями. В этом классе определены атрибуты, такие как название вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т.п. Класс поддерживает методы сравнения вакансий между собой по зарплате и валидацию данных, которыми инициализируются его атрибуты.  
3. Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл, получения данных из файла по указанным критериям и удаления информации о вакансиях. Класс для сохранения информации о вакансиях в JSON-файл. Дополнительно реализованы классы для работы с другими форматами, например с CSV- или Excel-файлом, с TXT-файлом.  
4. Функция для взаимодействия с пользователем через консоль. Возможность выбрать платформы вакансий, поиск по вакансиям, сортировка результатов.  
5. Все классы и функции объединены в единую программу.  