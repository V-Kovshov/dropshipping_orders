from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.db import CreateOrder

order = CreateOrder()


def get_inline_shoes(*args) -> InlineKeyboardMarkup:
	models_lst = list(*args)
	kb = InlineKeyboardBuilder()
	for model in models_lst:
		kb.add(InlineKeyboardButton(text=str(model), callback_data=str(model.id)))
	kb.adjust(1)
	return kb.as_markup()


def get_inline_size(sizes) -> InlineKeyboardMarkup:
	kb = InlineKeyboardBuilder()
	for size in sizes:
		kb.add(InlineKeyboardButton(text=str(size), callback_data=str(size.id)))
	kb.adjust(1)
	return kb.as_markup()
