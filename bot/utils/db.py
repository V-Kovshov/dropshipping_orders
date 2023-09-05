from asgiref.sync import sync_to_async
from django.db.models import Q

from bot.models import *
import logging

from bot.utils.nova_post_api import get_status_parcel

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


@sync_to_async
def get_all_balance(user_id) -> int:
    balance = 0
    user = UserTG.objects.get(tg_id=user_id)
    # fixme: решить как отмечать заказы с уже обработанными балансами (в админке - "Забран")
    orders = OrderTG.objects.filter(Q(user_id__tg_id=user_id) & Q(invoice__regex=r'\d{14}') & Q(completed_order=False))
    for order in orders:
        status = get_status_parcel(order.invoice)
        if status == 'Відправлення отримано':
            balance += order.balance
            order.completed_order = True
            order.save()
    user.balance += balance
    user.save()

    return int(user.balance)


def write_off_balance(user_id, summ) -> None:
    orders = OrderTG.objects.filter(Q(user_id=user_id) & Q(completed_order=True) &
                                    Q(balance__gt=0)).order_by('balance')
    flag, total = True, int(summ)
    while flag:
        for order in orders:
            if total < order.balance:
                order.balance -= total
                order.save()
                flag = False
            else:
                balance = order.balance
                order.balance -= total - (total - order.balance)
                total -= balance
                order.save()


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
    def get_size(self, size_id: int) -> str:
        size = SizeQuantity.objects.get(id=size_id)
        return f'{size.size}({size.centimeters}см)'

    @sync_to_async
    def check_balance(self, user_id: int) -> int:
        user = UserTG.objects.get(tg_id=user_id)
        user_balance = int(user.balance)
        return user_balance

    @sync_to_async
    def get_user_name(self, user_id: int) -> str:
        user = UserTG.objects.get(tg_id=user_id)
        user_name = str(user.name)
        return user_name

    @sync_to_async
    def create_order_from_balance(self, context_data: dict) -> None:
        user_id = UserTG.objects.get(tg_id=context_data.get('user_id'))
        model = Shoes.objects.get(id=context_data.get('model'))
        size = SizeQuantity.objects.get(id=context_data.get('shoes_size'))
        client_name = context_data.get('client_name')
        client_phone = context_data.get('client_phone')
        other_data = context_data.get('other_data')
        balance_advance = context_data.get('balance_advance') or context_data.get('pay')
        postpayment = context_data.get('postpayment') or 0
        balance = (int(balance_advance) + int(postpayment)) - model.price_opt

        OrderTG.objects.create(user_id=user_id,
                               shoes_model=model,
                               shoes_size=size.size,
                               client_name=client_name,
                               client_phone=client_phone,
                               other_data=other_data,
                               postpayment=postpayment,
                               balance_pay=balance_advance,
                               balance=balance)

        if size.quantity >= 1:
            size.quantity -= 1
            size.save()

        # user_id.balance -= int(balance_advance)
        # user_id.save()
        write_off_balance(user_id, balance_advance)

    @sync_to_async
    def create_order_payfull(self, context_data: dict) -> None:
        user_id = UserTG.objects.get(tg_id=context_data.get('user_id'))
        model = Shoes.objects.get(id=context_data.get('model'))
        size = SizeQuantity.objects.get(id=context_data.get('shoes_size'))
        client_name = context_data.get('client_name')
        client_phone = context_data.get('client_phone')
        other_data = context_data.get('other_data')
        screen = context_data.get('screen_url')
        if not context_data.get('pay'):
            payfull_advance, postpayment = 0, 0
        else:
            payfull_advance, postpayment = context_data.get('pay').split(',')
        balance = (int(payfull_advance) + int(postpayment)) - model.price_opt

        if payfull_advance:
            OrderTG.objects.create(user_id=user_id,
                                   shoes_model=model,
                                   shoes_size=size.size,
                                   client_name=client_name,
                                   client_phone=client_phone,
                                   other_data=other_data,
                                   screen_payment=screen,
                                   postpayment=postpayment,
                                   balance=balance)
        else:
            OrderTG.objects.create(user_id=user_id,
                                   shoes_model=model,
                                   shoes_size=size.size,
                                   client_name=client_name,
                                   client_phone=client_phone,
                                   other_data=other_data,
                                   screen_payment=screen)

        if size.quantity >= 1:
            size.quantity -= 1
            size.save()

    # @sync_to_async


