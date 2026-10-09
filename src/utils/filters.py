from typing import List, Tuple

from src.models.aeroplane import Aeroplane


def filter_aeroplanes(aeroplanes: List[Aeroplane], filter_words: List[str]) -> List[Aeroplane]:
    """Выборка самолетов по стране регистрации"""

    if not filter_words:
        return aeroplanes

    result_list = []
    for aeroplane in aeroplanes:
        # vacancy_dict = aeroplane.to_dict()
        for word in filter_words:
            if word.lower() in aeroplane.origin_country.lower():
                # print(word)
                # print(vacancy_dict)
                result_list.append(aeroplane)

    return result_list


def get_aeroplanes_by_altitude(aeroplanes: List[Aeroplane], altitude_range: Tuple[float, float]) -> List[Aeroplane]:
    """Выборка самолетов по диапазону высот"""

    if not altitude_range:
        return aeroplanes

    result_list = []
    for aeroplane in aeroplanes:
        if altitude_range[0] <= aeroplane.altitude <= altitude_range[1]:
            result_list.append(aeroplane)

    return result_list


def sort_aeroplanes(aeroplanes: List[Aeroplane]) -> List[Aeroplane]:
    """Сортировка по зарплате (по убыванию)"""

    aeroplanes.sort(key=lambda x: x.altitude, reverse=True)
    return aeroplanes


def get_top_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """Выборка нескольких самолетов с максимальной высотой"""

    top_aeroplanes = []
    for index, item in enumerate(aeroplanes):
        if index < top_n:
            top_aeroplanes.append(item)
        else:
            break

    return top_aeroplanes
