from database.models import HistoryReq, User, Offer


def add_to_history(user_id, offers, req_info) -> None:
    """
    Функция, добавляющая запрос и офферы в базу данных
    :param user_id: ID пользователя
    :param offers: Все офферы
    :param req_info: Краткая информация запроса
    :return: None
    """
    history = HistoryReq.create(
        user=user_id,
        req_info=req_info
    )
    history.save()
    for offer in offers:
        Offer.create(
            req=history,
            title=offer['title'],
            price=offer['price'],
            url=offer['url'],
            image=offer['image'],
            review_rating=offer['rating'],
            location=offer['location']
        )
