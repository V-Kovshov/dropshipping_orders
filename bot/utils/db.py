from asgiref.sync import sync_to_async
from bot.models import *
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(filename)s -> [LINE:%(lineno)d] -> %(levelname)-8s [%(asctime)s] -> %(message)s',
                    filename='bot/logging.log',
                    filemode='w')


@sync_to_async
def check_user_in_db(user_id) -> bool:
    try:
        user = UserTG.objects.get(tg_id=user_id)
        logging.info('Получили юзера')
        return True
    except:
        logging.info('Нет такого юзера')
        return False


@sync_to_async
def registration_user(context_data) -> None:
    tg_id = context_data.get('tg_id')
    name = context_data.get('name')
    username = context_data.get('username')
    phone = context_data.get('phone')
    bank_card = context_data.get('bank_card')
    balance = context_data.get('balance')

    UserTG.objects.create(tg_id=tg_id, name=name, username=username, phone=phone, bank_card=bank_card, balance=balance)


class Order:
    @sync_to_async
    def get_model_sizes(self, model_id: int) -> list:
        sizes = SizeQuantity.objects.filter(shoes=model_id)
        size_lst = []
        for size in sizes:
            size_lst.append(size)
        return size_lst

    @sync_to_async
    def check_article(self, article: str) -> list | bool:
        shoes = Shoes.objects.filter(article__icontains=article)
        return list(shoes) if shoes.count() >= 1 else False

    @sync_to_async
    def get_model(self, model_id: int) -> Shoes:
        shoes = Shoes.objects.get(id=model_id)
        return shoes

    @sync_to_async
    def get_balance(self, user_id: int):
        user = UserTG.objects.get(tg_id=user_id)
        user_balance = int(user.balance)
        return user_balance
