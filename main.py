from telebot import custom_filters

from filters.PriceRangeFilter import PriceRangeFilter
from filters.AmountFilter import AmountFilter
from database.models import create_models
from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    create_models()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(AmountFilter())
    bot.add_custom_filter(PriceRangeFilter())
    set_default_commands(bot)
    bot.infinity_polling()
