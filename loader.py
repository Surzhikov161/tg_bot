from telebot import TeleBot, StateMemoryStorage

from api.api_class import MyAPI
from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
API = MyAPI()
