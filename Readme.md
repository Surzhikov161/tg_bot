# TelegramBot
Телеграмм Бот для поиска товаров с сервиса Ebay.
![img.png](img.png)

### Технологии

- [pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/). Для создания телеграмм бота;
- [peewee](https://docs.peewee-orm.com/en/latest/) ORM. Для реализации моделей для хранения данных сервиса;
- [SQLite3](https://www.sqlite.org/). База Данных сервиса;
- [requests](https://www.sqlite.org/). Реализация API;

### Запуск

1. Клонируйте репозиторий
   командой ```git clone https://github.com/Surzhikov161/tg_bot.git)```
2. Настроить параметры окружения ([BOT_TOKEN](https://core.telegram.org/bots/tutorial), RAPID_API_KEY) в файле .env;
3. Запустить бота ```python main.py```.

*RAPID_API_KEY - API для получения товара
