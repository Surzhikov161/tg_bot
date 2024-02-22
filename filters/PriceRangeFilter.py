from telebot import SimpleCustomFilter
from utils.get_price import get_price


class PriceRangeFilter(SimpleCustomFilter):
    """
    Фильтер ввода пользователя.
    Проверяет является ли диапазон цены, введенный пользователем, корректным.

    :Arguments:
        key: Ключ для использования фильтра
    """
    key = 'price_range'

    def check(self, message):
        if len(get_price(message.text)) == 2:
            return True
        return False
