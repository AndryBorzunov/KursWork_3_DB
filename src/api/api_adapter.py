from requests import get

from src.api.air_abstract_api import AirAbstractAPI


class APIAdapter(AirAbstractAPI):

    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_aeroplanes(self, country: str) -> dict | None:
        # Заголовок
        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }

        # Указываем параметры: наименование страны, в каком формате возвращать данные и
        # максимальная длина списка стран в ответе
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        if response.status_code == 200:

            data = response.json()
            if len(data) == 0:
                raise TypeError(f"Нет данных по стране {country}")

            # Получаем координаты ограничивающего прямоугольника
            geo_coordinates = data[0].get("boundingbox")

            # Параметры для фильтрации самолетов по их географическим координатам
            params = {
                "lamin": geo_coordinates[0],
                "lamax": geo_coordinates[1],
                "lomin": geo_coordinates[2],
                "lomax": geo_coordinates[3],
            }

            response = get(url=self.opensky_url, params=params)

            if response.status_code == 200:
                self.aeroplanes = response.json()

        return self.aeroplanes
