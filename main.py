from src.api.api_adapter import APIAdapter
from src.models.aeroplane import Aeroplane
from src.utils.config import config
from src.utils.DBManager import DBManager


def print_countries_and_aeroplanes_count(countries: list[dict]) -> None:
    """
    Вывод на терминал наименования страны и количества самолетов
    """
    print("\n")
    for country in countries:
        print(f"{country['country']} - {country['count_aeroplanes']} самолетов")
    print("\n")


def print_aeroplanes(aeroplanes: list[dict]) -> None:
    """
    Вывод на терминал самолетов
    """
    print(
        "|     Страна     |    Идентификатор    |    Позывной     |   Регистрация      | Скорость, м/с | Высота, м |"
    )
    for aeroplane in aeroplanes:
        print(
            f"|  {aeroplane['country']}  | {aeroplane['icao24']}  |  {aeroplane['callsign']}  |   {aeroplane['origin_country']}   | {aeroplane['velocity']}  |  {aeroplane['altitude']} |"
        )

    print("\n")


def user_interaction():
    # country = input("Введите название страны: ")
    # api = APIAdapter()
    # aeroplanes = api.get_aeroplanes(country)
    # print(aeroplanes)
    #
    # aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
    # print(len(aeroplanes))
    #
    # for item in aeroplanes:
    #     if item.altitude < 0:
    #         print(item)
    #
    # filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    #
    # filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
    # for item in filtered_aeroplanes:
    #     print(item)

    countries = input("Введите название стран через запятую: ").split(",")
    countries = tuple(item.strip() for item in countries)
    countries = tuple(x for x in countries if x != "")
    api = APIAdapter()

    # Получаем данные
    data = []
    for country in countries:
        aeroplanes = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
        data.append({"country": country, "aeroplanes": aeroplanes})

    # print(data)

    # работа с БД

    # Считываем параметры. Файл по умолчанию - database.ini
    params = config()

    # Создаём класс DBManager. Загружаем список вакансий в базу данных
    db = DBManager("my_db", params, data)

    # Получаем список компаний и количество вакансий в каждой компании
    countries = db.get_countries_and_aeroplanes_count()
    print_countries_and_aeroplanes_count(countries)

    # Получаем  список всех самолетов
    aeroplanes = db.get_all_aeroplanes()
    print_aeroplanes(aeroplanes)

    # Получаем среднюю скорость по самолетам
    avg = db.get_avg_speed()
    print(f"Средняя скорость: {avg}")

    # Получаем вакансии с зарплатой выше средней
    aeroplanes_top = db.get_aeroplanes_with_higher_speed(avg)
    print("Список самолетов, у которых скорость выше средней: ")
    print_aeroplanes(aeroplanes_top)

    # Получаем список всех самолетов, в позывном которых содержатся переданные в метод символы
    keyword = input("Введите ключевое слово для поиска самолета: ")
    vacancies_keyword = db.get_aeroplanes_with_keyword(keyword)
    print(f"Воздушные суда, в позывных которых содержится слово {keyword}")
    print_aeroplanes(vacancies_keyword)


if __name__ == "__main__":
    user_interaction()
