from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, FloatField

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """
    Базовый класс.
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    Модель пользователя

    :Arguments:
        user_id: ID пользователя
        username: Никнейм пользователя
        first_name: Имя пользователя
        last_name: Фамилия пользователя(Если есть)
    """
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


class HistoryReq(BaseModel):
    """
    Модель историй запроса пользователя.
    :Arguments:
        user: Ссылка на модель пользователя
        req_info: Краткая информация о запросе.
    """
    user = ForeignKeyField(User, backref='history')
    req_info = CharField()

    def __str__(self):
        return f'{self.id}. {self.req_info}'


class Offer(BaseModel):
    """
    Модель предложения продукта.
    :Arguments:
        req: Ссылка на модель историй пользователя
        title: Название предложения
        price: Цена товара
        url: Ссылка на товар в магазине
        image: Фото товара
        review_rating: Рейтинг пользователя(Если есть)
        location: Локация продавца
    """
    req = ForeignKeyField(HistoryReq, backref='offers')
    title = CharField()
    price = CharField()
    url = CharField()
    image = CharField()
    review_rating = CharField(null=True)
    location = CharField()

    def __str__(self):
        return (f'{self.title}. Цена: {self.price}\n'
                f'Ссылка на товар: {self.url}\n')


def create_models() -> None:
    """
    Создает таблици в базе данных
    :return: None
    """
    db.create_tables(BaseModel.__subclasses__())
