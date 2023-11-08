from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class PaginationCallbackFactory(CallbackData, prefix='pag'):
	action: str
	page: int


def paginator(page: int = 0):
	kb = InlineKeyboardBuilder()
	kb.row(InlineKeyboardButton(text='⬅️', callback_data=PaginationCallbackFactory(action='prev')))
	kb.row(InlineKeyboardButton(text='➡️', callback_data=PaginationCallbackFactory(action='next')))



def all_orders_kb(*args) -> InlineKeyboardMarkup:
	orders_lst = list(*args)
	kb = InlineKeyboardBuilder()
	cnt = 1
	for order in orders_lst:
		kb.add(InlineKeyboardButton(text=f'{cnt}. {order.client_name}', callback_data=order.id))
		cnt += 1
	kb.adjust(1)

	return kb.as_markup()


def found_orders_kb(*args) -> InlineKeyboardMarkup:
	orders_lst = list(*args)
	kb = InlineKeyboardBuilder()
	cnt = 1
	for order in orders_lst:
		kb.add(InlineKeyboardButton(
			text=f'{cnt}. {order.date} | {order.client_name}',
			callback_data=order.id
		))
		cnt += 1
	kb.adjust(1)

	return kb.as_markup()

