from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def all_orders_kb(*args) -> InlineKeyboardMarkup:
	orders_lst = list(*args)
	kb = InlineKeyboardBuilder()
	for order in orders_lst:
		kb.add(InlineKeyboardButton(text=order.client_name, callback_data=order.id))
	kb.adjust(1)

	return kb.as_markup()


def found_orders_kb(*args) -> InlineKeyboardMarkup:
	pass
