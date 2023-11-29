from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class PaginationCallbackFactory(CallbackData, prefix='pag'):
	action: str
	page: int


def paginator(page: int = 1):
	kb = InlineKeyboardBuilder()
	kb.row(
		InlineKeyboardButton(text='⬅️', callback_data=PaginationCallbackFactory(action='prev', page=page).pack()),
		InlineKeyboardButton(text='➡️', callback_data=PaginationCallbackFactory(action='next', page=page).pack()),
		width=2
	)

	return kb.as_markup()


def all_orders_kb(arr, total_pages, page: int = 1) -> InlineKeyboardMarkup:
	orders_lst = [*arr]
	kb = InlineKeyboardBuilder()

	cnt = 1 if page == 1 else (page * 3) - 2
	for order in orders_lst:
		kb.add(InlineKeyboardButton(text=f'[{cnt}] {order.client_name}', callback_data=f'ord_{order.id}'))
		cnt += 1
	kb.adjust(1)
	kb.row(
		InlineKeyboardButton(text='⬅️', callback_data=PaginationCallbackFactory(action='prev', page=page).pack()),
		InlineKeyboardButton(text=f'Стр.: {page}/{total_pages}', callback_data='#'),
		InlineKeyboardButton(text='➡️', callback_data=PaginationCallbackFactory(action='next', page=page).pack()),
		width=3
	)

	return kb.as_markup()


def found_orders_kb(*args) -> InlineKeyboardMarkup:
	orders_lst = list(*args)
	kb = InlineKeyboardBuilder()
	cnt = 1
	for order in orders_lst:
		kb.add(InlineKeyboardButton(
			text=f'{cnt}. {order.date} | {order.client_name}',
			callback_data=f'ord_{order.id}'
		))
		cnt += 1
	kb.adjust(1)

	return kb.as_markup()
