from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_inline_shoes(*args):
	models_lst = list(*args)
	kb = InlineKeyboardBuilder()
	for model in models_lst:
		kb.add(InlineKeyboardButton(text=str(model), callback_data=model.slug))
	kb.adjust(1)
	return kb.as_markup()
