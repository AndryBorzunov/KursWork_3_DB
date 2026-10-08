from abc import ABC, abstractmethod
from typing import Any


class AirAbstractAPI(ABC):
    """ Абстрактный класс для работы с API opensky-network.org """

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[dict] | None:
        """Получение вакансий по поисковому запросу"""
        pass
