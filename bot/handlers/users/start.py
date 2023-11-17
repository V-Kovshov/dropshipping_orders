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
    await msg.answer(
        f"Вітаємо вас в боті &#127801<b>Roza Shoes</b>&#127801\r\n\nОберіть потрібний потрібний вам пункт:",
        reply_markup=reply.start_keyboard())


@router.message(F.text == 'Підтримка🤝')
async def get_support(msg: types.Message, bot: Bot) -> None:
    data = "🔺<b>Реквізити</b>🔺\n"\
        "<b>Установа банку:</b> ПриватБанк\n\n" \
        "<b>МФО банку:</b> 305299\n\n" \
        "<b>Одержувач платежу:</b>\n" \
        "ФОП ДЕМКІВ АЛІНА РУСЛАНІВНА\n\n" \
        "<b>IBAN:</b>\nUA513515330000026007052157707\n\n" \
        "<b>Рахунок отримувача:</b>\n26007052157707\n\n" \
        "<b>РНУКПН одержувача:</b>\n3260704780\n\n" \
        "<b>Призначення платежу:</b>\nОплата за товар і ПРІЗВИЩЕ КЛІЄНТА\n\n" \
        "💌<b>Зв'язатися з менеджером:</b>\n@roza_shoes_drop"
    await msg.answer(data, reply_markup=reply.start_keyboard())
