from telebot.types import Message

from database.models import User
from keyboards.inline.sort_type import sort_markup
from loader import bot, API
from states.param_states import BotStates
from utils.add_to_history import add_to_history
from utils.get_price import get_price
from utils.show_offers import show_offers
import re


@bot.message_handler(commands=['low', 'high', 'custom'])
def low_high_custom(message: Message) -> None:
    """
    Функция поиска товара на Ebay по заданным пользователем характеристикам.
    :param message: Сообщение пользователя.
    :return: None
    """
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "😢Вы не зарегистрированы. Напишите /start")
        return
    if message.text == '/custom':
        bot.set_state(message.from_user.id, BotStates.price_range, message.chat.id)
        bot.send_message(message.chat.id, 'Введите диапазон цены')
    else:
        bot.set_state(message.from_user.id, BotStates.product, message.chat.id)
        bot.send_message(message.chat.id, 'Какой товар вы хотите найти?(Желательно на английском языке)')
    with bot.retrieve_data(message.from_user.id) as data:
        data["sort"] = True if message.text == '/high' else False
        data['price_range'] = None
        data['req_info'] = message.text


@bot.message_handler(state='*', commands=['cancel'])
def cancel(message: Message) -> None:
    """
    Сброс поиска.
    :param message: Сообщение пользователя.
    :return: None
    """
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=BotStates.price_range, price_range=True)
def get_price_range(message: Message) -> None:
    """
    Спрашивает у пользователя какую применить сортировку.
    И добавляет в storage диапазон цены.
    :param message: Сообщение пользователя.
    :return: None
    """
    with bot.retrieve_data(message.from_user.id) as data:
        data["price_range"] = get_price(message.text)
        data['req_info'] = data['req_info'] + f' Диапазон цены(${data["price_range"][0]} - ${data["price_range"][1]})'
    bot.send_message(message.chat.id, 'Какую сортировку применить?', reply_markup=sort_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_sort(call) -> None:
    """
    Применяет сортировку, выбранную пользователем
    :param call: Элемент, на который нажал пользователь
    :return: None
    """
    if call.data == 'asc':
        bot.answer_callback_query(call.id, "Применена сортировка по возрастанию цены")
        with bot.retrieve_data(call.from_user.id) as data:
            data["sort"] = False
            data['req_info'] = data['req_info'] + ', Сортировка по возрастанию цены'
    elif call.data == 'desc':
        bot.answer_callback_query(call.id, "Применена сортировка по убыванию цены")
        with bot.retrieve_data(call.from_user.id) as data:
            data["sort"] = True
            data['req_info'] = data['req_info'] + ' (сортировка по убыванию цены)'
    bot.send_message(call.from_user.id, 'Какой товар вы хотите найти?(Желательно на английском языке)')
    bot.set_state(call.from_user.id, BotStates.product, call.from_user.id)


@bot.message_handler(state=BotStates.price_range, price_range=False)
def incorrect_price_range(message: Message) -> None:
    """
    Функция, проверяющая правильность ввода диапазона цены.
    :param message: Сообщение пользователя.
    :return: None
    """
    bot.send_message(message.chat.id,
                     '😢Упс... Вы ввели неверный диапазон. Пожалуйста введите число!\n(Пример: 15 - 30)')


@bot.message_handler(state=BotStates.product)
def get_product(message: Message) -> None:
    """
    Функция, спрашивающая у пользователя количество товаров.
    И добавляет в storage название товара.
    :param message: Сообщение пользователя.
    :return: None
    """
    bot.send_message(message.chat.id, 'Количество единиц товара?')
    bot.set_state(message.from_user.id, BotStates.get_offers, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data["product"] = message.text
        #
        data['req_info'] = re.sub(r'/\w+', re.match(r'/\w+', data['req_info']).group(0) + f' Товар:{message.text}',
                                  data['req_info'])


@bot.message_handler(state=BotStates.get_offers, correct_amount=True)
def get_content(message: Message) -> None:
    """
    Функция, отображает пользователю найденые предложения по его параметрам.
    :param message: Сообщение пользователя.
    :return:None
    """

    with bot.retrieve_data(message.from_user.id) as data:
        data["amount"] = message.text
        data['req_info'] = re.sub(data['product'],
                                  re.findall(data['product'], data['req_info'])[
                                      0] + f' в количестве {message.text}.',
                                  data['req_info'])
    bot.send_message(message.chat.id, 'Подождите немного, я собираю подходящие предложения...')
    try:

        offers = API.send_request(product=data['product'], amount=int(data['amount']), reverse=data['sort'],
                                  price_range=data['price_range'])
        show_offers(offers, message.chat.id)
        add_to_history(user_id=message.from_user.id, offers=offers, req_info=data['req_info'])

    except Exception:
        bot.send_message(message.chat.id, '😔Упс... Произошла ошибка. Повторите запрос заново.')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=BotStates.get_offers, correct_amount=False)
def incorrect_amount(message: Message) -> None:
    """
    Проверка параметра числа товаров.
    :param message: Сообщение пользователя.
    :return: None
    """
    bot.send_message(message.chat.id,
                     '😢Упс... Вы ввели не числовое значение или число, меньшее нуля. Пожалуйста введите число!')
