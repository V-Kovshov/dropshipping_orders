import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'dropshipping_orders.settings'
django.setup()

from bot.keyboards.base import reply

import logging

from aiogram import types, Bot, Router, F
from aiogram.filters import Command, CommandStart


router = Router()


@router.message(CommandStart())
async def get_start(msg: types.Message, bot: Bot) -> None:
	await msg.answer(f"Вітаємо вас в боті &#127801<b>Roza Shoes</b>&#127801\r\n\nОберіть потрібний потрібний вам пункт:",
					reply_markup=reply.start_keyboard())
