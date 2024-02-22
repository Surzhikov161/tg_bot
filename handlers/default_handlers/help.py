from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
    Справка о боте.
    :param message: Сообщение пользователя
    :return: None
    """
    bot.reply_to(message, 'Привет, я бот по поиску товаров на Ebay!'
                          '\nВот все возможные команды:'
                          '\n\t-/low -- Вывод предложений искомого товара с минимальными ценами.'
                          '\n\t-/high -- Вывод предложений искомого товара с максимальными ценами.'
                          '\n\t-/custom -- Вывод искомого товаров в указанном диапазоне цены.'
                          '\n\t-/history -- Последние 10 запросов пользователя.'
                          '\n\t-/cancel -- Отменить текущую команду.'
                 )
