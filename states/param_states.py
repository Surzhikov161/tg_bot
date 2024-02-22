from telebot.handler_backends import State, StatesGroup


class BotStates(StatesGroup):
    """
    Класс состояний бота
    """
    product = State()
    price_range = State()
    get_offers = State()
    show_offers = State()
