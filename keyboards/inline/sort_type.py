from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def sort_markup() -> InlineKeyboardMarkup:
    """
    Создает макет кнопок для сортировки.
    :return: Макет кнопок
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('По Возрастанию Цены', callback_data='asc'),
               InlineKeyboardButton('По Убыванию Цены', callback_data='desc'))
    return markup
