import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'dropshipping_orders.settings'
django.setup()

from bot.models import Shoes, SizeQuantity
from bot.keyboards.base import reply
from bot.utils import db

import logging

from aiogram import types, Bot, Router, F
from aiogram.filters import Command, CommandStart
from asgiref.sync import sync_to_async


router = Router()


@router.message(CommandStart())
async def get_start(msg: types.Message, bot: Bot) -> None:
	await msg.answer(f"Вітаємо вас в боті &#127801<b>Roza Shoes</b>&#127801!\r\nОберіть потрібний потрібний вам пункт:",
					reply_markup=reply.start_keyboard())


# @router.message(F.text == 'Оформити замовлення')
# async def get_shoes(msg: types.Message, bot: Bot):
# 	logging.info('Enters in func')
# 	shoes = await Shoes.objects.aget(article='Модель к1703п лаванда')
# 	# async for i in shoes.sizequantity_set.filter(shoes=shoes):
# 	# 	print(i)
# 	size = await db.get_size(shoes)
# 	for s in size:
# 		print(s)
