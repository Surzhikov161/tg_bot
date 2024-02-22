from config_data import config
from typing import Optional, List
import requests
import json
import re

from utils.get_price import get_price


class MyAPI:
    """
    Класс API. Для отправки запроса на сервер и
    обработки результата.

    :Arguments:
        __URL: url сервера
        __HEADERS: параметры запроса
    """
    __URL = "https://ebay-search-result.p.rapidapi.com/search/{}"
    __HEADERS: dict[str, str] = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "ebay-search-result.p.rapidapi.com"
    }

    def send_request(self, product: str, amount: int, reverse: bool = False,
                     price_range: Optional[List[float]] = None) -> List[dict]:
        """
        Метод отправки и обработки запроса
        :param product: Название товара
        :param amount: Кол-во товара
        :param reverse: Тип сортировки
        :param price_range: Диапазон цены
        :return: Обработанный JSON ответ.
        """
        response = requests.get(self.__URL.format(re.sub(' ', r'%20', product)), headers=self.__HEADERS)
        if response.status_code == 200:
            content = sorted(json.loads(response.text)['results'], key=lambda d: float(get_price(d['price'])[0]),
                             reverse=reverse)
            show_offers_len = amount if amount < len(content) else len(content)
            if price_range:
                return list(
                    filter(lambda d: price_range[0] <= get_price(d['price'])[0] <= price_range[1],
                           content))[:show_offers_len]
            return content[:show_offers_len]
        else:
            print('Ошибка запроса!')
