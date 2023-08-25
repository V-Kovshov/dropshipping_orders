from asgiref.sync import sync_to_async
from bot.models import *


@sync_to_async
def check_client_phone(phone: str) -> bool:
	if 9 < len(phone) < 11:
		for item in phone:
			if not item.isdigit():
				return False
		return True
	return False


@sync_to_async
def check_pay_sum(amount: str) -> bool:
	if len(amount) >= 3:
		for item in amount:
			if not item.isdigit():
				return False
		return True
	return False


@sync_to_async
def check_shoes_price(model_id: int, price: str) -> bool:
	price = int(price)
	shoes = Shoes.objects.get(id=model_id)
	if shoes.price_opt > price:
		return True
	return False

