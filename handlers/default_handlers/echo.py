from loader import bot
from telebot.types import Message


@bot.message_handler(func=lambda message: True)
def echo(message: Message) -> None:
    """
    Ответ на любое сообщение пользователя, которое не прописанно в функционале бота.
    :param message: Сообщение пользователя
    :return: None
    """
    bot.send_message(message.from_user.id, 'Неизвестная комманада. Напишите /help для справки.')
