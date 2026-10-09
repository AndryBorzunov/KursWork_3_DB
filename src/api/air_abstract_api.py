from abc import ABC, abstractmethod


class AirAbstractAPI(ABC):
    """Абстрактный класс для работы с API opensky-network.org"""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> dict | None:
        """Получение вакансий по поисковому запросу"""
        pass
