from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class PaginationCallbackFactory(CallbackData, prefix='pag'):
	action: str
	page: int


def all_orders_kb(arr, total_pages, page: int = 1) -> InlineKeyboardMarkup:
	orders_lst = [*arr]
	kb = InlineKeyboardBuilder()

	cnt = 1 if page == 1 else (page * 10) - 9
	for order in orders_lst:
		date = f'{order.date.day}-{order.date.month if order.date.month > 9 else f"0{order.date.month}"}-{order.date.year}'
		kb.add(InlineKeyboardButton(text=f'{cnt}. {date} | {order.client_name}', callback_data=f'ord_{order.id}'))
		cnt += 1
	kb.adjust(1)
	kb.row(
		InlineKeyboardButton(text='⬅️', callback_data=PaginationCallbackFactory(action='prev', page=page).pack()),
		InlineKeyboardButton(text=f'Стр.: {page}/{total_pages}', callback_data='#'),
		InlineKeyboardButton(text='➡️', callback_data=PaginationCallbackFactory(action='next', page=page).pack()),
		width=3
	)
	kb.row(
		InlineKeyboardButton(text='Назад', callback_data='back')
	)

	return kb.as_markup()


def back_btn(*args) -> InlineKeyboardMarkup:
	kb = InlineKeyboardBuilder()

	kb.add(InlineKeyboardButton(text='Назад', callback_data='back'))

	return kb.as_markup()
