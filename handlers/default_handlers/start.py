from peewee import IntegrityError
from telebot.types import Message
from database.models import User
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Начало работы бота.
    :param message: Сообщение пользователя
    :return: None
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(message, f'😊Добро пожаловать в бот по поиску товаров на Ebay, {username}')
    except IntegrityError:
        bot.reply_to(message, f'😊Рад вас снова видеть, {username}!')
