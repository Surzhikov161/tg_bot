from typing import List

from loader import bot


def show_offers(offers: List, chat_id) -> None:
    """
    Вывод всех найденных офферов пользователю
    :param offers: Список офферов
    :param chat_id: ID чата
    :return: None
    """
    if len(offers) == 0:
        bot.send_message(chat_id, '😔Увы... По вашемму запросу ничего не найдено.')
        return
    for i, offer in enumerate(offers):
        bot.send_message(chat_id, f'{i + 1}. {offer["title"]}')
        try:
            bot.send_photo(chat_id, offer['image'])
        except Exception:
            bot.send_message(chat_id, '😔К сожалению, Не получилось загрузить фото.')
        bot.send_message(chat_id, 'Цена: {}\n'
                                  'Рейтинг продавца: {}\n'
                                  'Доставка из: {}\n'
                                  'Ссылка на товар: {}'.format(offer["price"], offer["rating"], offer['location'],
                                                               offer["url"]))
