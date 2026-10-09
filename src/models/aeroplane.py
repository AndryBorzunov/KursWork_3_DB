from typing import Any


class Aeroplane:
    """Класс представляет абстракцию самолета"""

    def __init__(self, icao24: str, callsign: str, origin_country: str, velocity: float, altitude: float) -> None:
        # уникальный идентификатор борта
        self.__ICAO24 = Aeroplane.__verify_string(icao24)

        # позывной рейса
        self.__Callsign = Aeroplane.__verify_string(callsign)

        # Страна регистрации ВС
        self.__origin_country = Aeroplane.__verify_country(origin_country)

        # горизонтальная скорость (м/с)
        self.__velocity = Aeroplane.__verify_velocity(velocity)

        # геометрическая высота (м)
        self.__altitude = Aeroplane.__verify_float(altitude)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, (float, Aeroplane)):
            raise TypeError("Операнд справа должен иметь тип float или Aeroplane")

        sc = other if isinstance(other, float) else other.altitude
        return self.altitude < sc

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, (float, Aeroplane)):
            raise TypeError("Операнд справа должен иметь тип float или Aeroplane")

        sc = other if isinstance(other, float) else other.altitude
        return self.altitude > sc

    def __repr__(self) -> str:
        return f"Позывной рейса: {self.__Callsign}, страна регистрации: {self.__origin_country}, скорость: {self.__velocity}, высота: {self.__altitude}"

    def __str__(self) -> str:
        return (
            "{"
            + f"Позывной рейса: {self.__Callsign}, страна регистрации: {self.__origin_country}, скорость: {self.__velocity}, высота: {self.__altitude}"
            + "}"
        )

    @classmethod
    def __verify_string(cls, value: str) -> str:
        """Верификация строки данных"""
        if not isinstance(value, str):
            raise TypeError("Значение должно иметь тип string")
        value = value.strip()
        if not value:
            print(value)
            value = "111"
            # raise TypeError("Значение не может быть пустым")
        cleaned = "".join(value.split())
        cleaned = cleaned.replace("'", "")
        if not cleaned.isalnum() or len(cleaned) == 0:
            raise TypeError("Значение может иметь только буквы и цифры")
        return value

    @classmethod
    def __verify_country(cls, value: str) -> str:
        """Верификация строки данных"""
        if not isinstance(value, str):
            raise TypeError("Значение должно иметь тип string")
        value = value.strip()
        if not value:
            raise TypeError("Значение не может быть пустым")
        cleaned = "".join(value.split())
        cleaned = cleaned.replace("'", "")
        if not cleaned.isalnum() or len(cleaned) == 0:
            print(value)
            raise TypeError("Значение может иметь только буквы и цифры")
        return value

    @classmethod
    def __verify_float(cls, value: float | None) -> float:
        """Верификация числового значения"""
        result = 0.0 if value is None else value
        if not isinstance(result, (float, int)):
            raise TypeError("Значение должно быть числом")
        return result

    @classmethod
    def __verify_velocity(cls, value: float | None) -> float:
        """Верификация числового значения"""
        result = 0.0 if value is None else value
        if not isinstance(result, (float, int)):
            raise TypeError("Значение должно быть числом")
        if result < 0.0:
            raise TypeError("Значение не может быть меньше нуля")
        return result

    @classmethod
    def cast_to_object_list(cls, aeroplanes: dict) -> list[Any] | None:
        """Преобразование списка словарей вакансий в список экземпляров класса Aeroplane"""

        aeroplanes_obj: list[Aeroplane] = []
        # parsed = json.loads(aeroplanes)
        # time_server = aeroplanes["time"]
        states = aeroplanes["states"]

        if states is None:
            return aeroplanes_obj

        for item in states:
            # Создаём объект и добавляем его в список
            aeroplane = Aeroplane(item[0], item[1].strip(), item[2], item[9], item[13])
            aeroplanes_obj.append(aeroplane)

        return aeroplanes_obj

    @property
    def icao24(self) -> str:
        return self.__ICAO24

    @property
    def callsign(self) -> str:
        return self.__Callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def altitude(self) -> float:
        return self.__altitude
