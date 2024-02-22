from typing import List

from telebot.types import Message

from loader import bot
from database.models import User, HistoryReq, Offer
from states.param_states import BotStates


@bot.message_handler(commands=['history'])
def show_history(message: Message) -> None:
    """
    Показывает последние 10 запросов пользователя
    :param message: Сообщение пользователя.
    :return: None
    """
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "😢Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(message.chat.id, '⬇️Ваши последние 10 запросов:⬇️')
    last_reqs: List[HistoryReq] = user.history.order_by(-HistoryReq.id).limit(10)
    result = []
    result.extend(map(str, reversed(last_reqs)))
    if not result:
        bot.send_message(message.from_user.id, "У вас еще нет задач")
        return
    result.append("\nВведите номер истории, чтобы показать ее предложения.\n"
                  "Или нажмите /cancel, чтобы пропустить этот шаг")
    bot.send_message(message.from_user.id, "\n".join(result))
    bot.set_state(message.from_user.id, BotStates.show_offers, message.chat.id)


@bot.message_handler(state=BotStates.show_offers)
def show_offers(message: Message) -> None:
    """
    Показывает все предложения определенной истории.
    :param message: Сообщение пользователя.
    :return: None
    """

    history_id = int(message.text)

    history = HistoryReq.get_or_none(HistoryReq.id == history_id)
    if history is None:
        bot.send_message(message.from_user.id, "Истории с таким ID не существует.")
        return
    else:
        offers: List[Offer] = history.offers
        result = []
        result.extend(map(str, offers))
        bot.send_message(message.from_user.id, "\n".join(result))
