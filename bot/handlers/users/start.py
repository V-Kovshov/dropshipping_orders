import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'dropshipping_orders.settings'
django.setup()

from bot.models import Shoes, SizeQuantity, UserTG
from bot.keyboards.base import reply
from bot.utils.db import check_user_in_db

import logging

from aiogram import types, Bot, Router, F
from aiogram.filters import Command, CommandStart
from asgiref.sync import sync_to_async


router = Router()


@router.message(CommandStart())
async def get_start(msg: types.Message, bot: Bot) -> None:
	await msg.answer(f"Вітаємо вас в боті &#127801<b>Roza Shoes</b>&#127801!\r\nОберіть потрібний потрібний вам пункт:",
					reply_markup=reply.start_keyboard())


@router.message(F.text == 'Оформити замовлення')
async def get_shoes(msg: types.Message, bot: Bot):
	user_id = msg.from_user.id
	user_in_db = await check_user_in_db(user_id=user_id)
	if user_in_db > 0:
		pass
	else:
		user_msg = 'Для початку давай зареєструємо твій обліковий запис\n\n' \
					'Щоб почати реєстрацію - натисніть /registration'
		await msg.answer(user_msg)
