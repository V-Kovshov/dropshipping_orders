from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import async_to_sync

from bot.utils.db import Order

order = Order()


def get_inline_shoes(*args):
	models_lst = list(*args)
	kb = InlineKeyboardBuilder()
	for model in models_lst:
		kb.add(InlineKeyboardButton(text=str(model), callback_data=str(model.id)))
	kb.adjust(1)
	return kb.as_markup()


def get_inline_size(sizes):
	kb = InlineKeyboardBuilder()
	for size in sizes:
		kb.add(InlineKeyboardButton(text=str(size), callback_data=str(size.id)))
	kb.adjust(1)
	return kb.as_markup()
