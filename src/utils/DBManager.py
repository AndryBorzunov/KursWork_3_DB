import psycopg2
from psycopg2 import Error
from psycopg2.extensions import connection, cursor

from src.models.aeroplane import Aeroplane


class DBManager:
    """
    Класс позволяет работать с БД PostreSQL.
    Сохраняет полученные данные о странах и самолетах, находящихся на территории этих стран в таблицы БД
    Реализованы функции для получения данных из БД
    """

    __params: dict
    __db_name: str

    def __init__(self, db_name: str, params: dict, data: list[dict[str, list[Aeroplane]]]) -> None:
        """
        Инициализация класса. Если база данных не существует, то создаёт её.
        Удаляет старые данные из таблиц и заполняет новыми данными
        :param db_name: имя базы данных
        :param params: параметры для подключения к базе данных
        :param data: данные о самолетах
        """

        conn: connection
        cur: cursor

        self.__params = params
        self.__db_name = db_name

        try:
            conn = psycopg2.connect(dbname="postgres", **params)
            conn.autocommit = True  # set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            print("Соединение установлено!")

            # Создаём БД
            self.__create_db(db_name, conn)
            conn.close()

            # Создаём таблицы
            conn = psycopg2.connect(dbname=db_name, **params)
            self.__create_table_countries(conn)
            self.__create_table_aeroplanes(conn)

            # Заполняем таблицы данными
            self.__save_data_to_database(data, conn)

        except (Exception, Error) as error:
            print("Ошибка", error)

        finally:
            if conn:
                cur.close()
                conn.close()

    @classmethod
    def __check_exist_db(cls, db_name: str, conn: connection) -> bool:
        """Проверка наличия БД"""

        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            return cur.fetchone() is not None

    @classmethod
    def __check_exist_table(cls, table_name: str, conn: connection) -> bool:
        """Проверка наличия таблицы"""

        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass(%s)", (table_name,))
            rows = cur.fetchone()
            # print(rows)
            if rows is not None:
                return rows[0] is not None
            else:
                return False

    @classmethod
    def __create_db(cls, db_name: str, conn: connection) -> None:
        """Создание БД"""

        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database;")  # WHERE datistemplate=false"))
            # rows = cur.fetchall()
            # print(rows)

            # Проверка наличия БД
            is_exist = cls.__check_exist_db(db_name, conn)
            # print(is_exist)
            if not is_exist:
                # Создаём базу данных
                cur.execute(f"CREATE DATABASE {db_name}")

        conn.commit()

    @classmethod
    def __create_table_countries(cls, conn: connection) -> None:
        """Создание таблицы countries - справочник стран"""

        with conn.cursor() as cur:
            # Проверка наличия таблицы
            is_exist = cls.__check_exist_table("countries", conn)
            # print(is_exist)
            if not is_exist:
                # Создаём таблицу
                # print("Создаём таблицу countries")
                cur.execute("""
                    CREATE TABLE countries (
                    country_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                    )
                    """)
            else:
                # Удалим данные из таблицы
                cur.execute("TRUNCATE TABLE countries RESTART IDENTITY CASCADE")

        conn.commit()

    @classmethod
    def __create_table_aeroplanes(cls, conn: connection) -> None:
        """Создание таблицы aeroplanes - самолеты в воздушном пространстве стран"""

        with conn.cursor() as cur:
            # Проверка наличия таблицы
            is_exist = cls.__check_exist_table("aeroplanes", conn)
            # print(is_exist)
            if not is_exist:
                # Создаём таблицу
                # print("Создаём таблицу aeroplanes")
                cur.execute("""
                      CREATE TABLE aeroplanes (
                      aeroplane_id SERIAL PRIMARY KEY,
                      country_id INT,
                      icao24 VARCHAR(255) NOT NULL,
                      callsign VARCHAR(255),
                      origin_country VARCHAR(255),
                      velocity FLOAT,
                      altitude FLOAT,
                      FOREIGN KEY (country_id) REFERENCES countries(country_id)
                      )
                    """)
                conn.commit()
            else:
                # Удалим данные из таблицы
                cur.execute("TRUNCATE TABLE aeroplanes RESTART IDENTITY")

    @classmethod
    def __save_data_to_database(cls, data: list[dict[str, list[Aeroplane]]], conn: connection) -> None:
        """Сохранение данных в базу данных"""

        with conn.cursor() as cur:

            for country in data:

                cur.execute(
                    """
                    INSERT INTO countries (name)
                    VALUES (%s)
                    RETURNING country_id
                    """,
                    (country["country"],),
                )
                country_id = cur.fetchone()[0]

                for aeroplane in country["aeroplanes"]:

                    cur.execute(
                        """
                        INSERT INTO aeroplanes (country_id, icao24, callsign, origin_country, velocity, altitude)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            country_id,
                            aeroplane.icao24,
                            aeroplane.callsign,
                            aeroplane.origin_country,
                            aeroplane.velocity,
                            aeroplane.altitude,
                        ),
                    )

        conn.commit()

    def get_countries_and_aeroplanes_count(self) -> list[dict]:
        """
        Получить список всех стран и количество самолетов в их воздушных пространствах
        """
        result = []
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT countries.name, COUNT(aeroplanes.*) FROM countries
                JOIN aeroplanes USING(country_id)
                GROUP BY countries.name
                """)
            # JOIN vacancies USING(employer_id)
            rows = cur.fetchall()

            for row in rows:
                result.append({"country": row[0], "count_aeroplanes": row[1]})

        conn.close()
        return result

    def get_all_aeroplanes(self) -> list[dict]:
        """
        Получить список всех самолетов с указанием названия страны,
        в воздушном пространстве которой он находится
        позывного, страны регистрации, скорости и высоты
        """

        result = []
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT с.name, a.icao24, a.callsign, a.origin_country, a.velocity, a.altitude
                FROM countries as с
                JOIN aeroplanes as a USING(country_id)
                """)

            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {
                        "country": row[0],
                        "icao24": row[1],
                        "callsign": row[2],
                        "origin_country": row[3],
                        "velocity": row[4],
                        "altitude": row[5],
                    }
                )

        conn.close()
        return result

    def get_avg_speed(self) -> float:
        """
        Получаем среднюю скорость по самолетам.
        """
        result: float = 0.0
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(velocity) FROM aeroplanes
                """)

            result = float(cur.fetchone()[0])

        conn.close()
        return result

    def get_aeroplanes_with_higher_speed(self, speed_min: float) -> list[dict]:
        """
        Получаем список всех самолетов, у которых скорость выше средней.
        """

        result = []
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT с.name, a.icao24, a.callsign, a.origin_country, a.velocity, a.altitude
                FROM countries as с
                JOIN aeroplanes as a USING(country_id)
                WHERE a.velocity > %s
                """,
                (speed_min,),
            )

            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {
                        "country": row[0],
                        "icao24": row[1],
                        "callsign": row[2],
                        "origin_country": row[3],
                        "velocity": row[4],
                        "altitude": row[5],
                    }
                )

        conn.close()
        return result

    def get_aeroplanes_with_keyword(self, keywords: str) -> list[dict]:
        """
        Получаем список всех самолетов, в позывном которых содержатся переданные в метод символы.
        """

        result = []
        conn = psycopg2.connect(dbname=self.__db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT с.name, a.icao24, a.callsign, a.origin_country, a.velocity, a.altitude
                FROM countries as с
                JOIN aeroplanes as a USING(country_id)
                WHERE a.callsign LIKE %s
                """,
                (f"%{keywords.upper()}%",),
            )

            rows = cur.fetchall()
            for row in rows:
                result.append(
                    {
                        "country": row[0],
                        "icao24": row[1],
                        "callsign": row[2],
                        "origin_country": row[3],
                        "velocity": row[4],
                        "altitude": row[5],
                    }
                )

        conn.close()
        return result
