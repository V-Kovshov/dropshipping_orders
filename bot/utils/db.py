from asgiref.sync import sync_to_async
from bot.models import *


@sync_to_async
def get_size(shoes) -> list:
    size_quantity = SizeQuantity.objects.filter(shoes=shoes)
    size_list = []
    for size in size_quantity:
        size_list.append(size)
    return size_list
