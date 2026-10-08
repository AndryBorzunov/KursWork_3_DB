from src.api.api_adapter import APIAdapter
from src.models.aeroplane import Aeroplane
from src.utils.filters import filter_aeroplanes


def user_interaction():
    country = input("Введите название страны: ")
    api = APIAdapter()
    aeroplanes = api.get_aeroplanes(country)
    print(aeroplanes)

    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes)
    print(len(aeroplanes))

    for item in aeroplanes:
        if item.altitude < 0:
            print(item)

    filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
    for item in filtered_aeroplanes:
        print(item)



if __name__ == "__main__":
    user_interaction()
