from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('Переменные окружения не загружены, так как отстутсвтует файл .env')
else:
    load_dotenv()

DB_PATH = os.path.relpath(os.path.join('database', 'database.db'))

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ('help', 'Справка'),
    ('cancel', 'Отмена команды')
)
