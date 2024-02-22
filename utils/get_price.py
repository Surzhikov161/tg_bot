import re
from typing import List


def get_price(price_str: str) -> List[float]:
    """
    Функция возвращает список диапазона цены.
    :param price_str: Строка диапазона
    :return: Cписок диапазона цены
    """
    pattern = re.compile(r'\d+[.]?\d+')
    price_list = re.findall(pattern, price_str)
    return sorted(list(map(float, price_list)))
