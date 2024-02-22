from telebot import SimpleCustomFilter


class AmountFilter(SimpleCustomFilter):
    """
    Фильтер ввода пользователя.
    Проверяет является ли положительным числом ввод пользователя.

    :Arguments:
        key: Ключ для использования фильтра
    """
    key = 'correct_amount'

    def check(self, message):
        if message.text.isdigit() and int(message.text) > 0:
            return True
        return False
