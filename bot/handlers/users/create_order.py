import logging

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from bot.keyboards.base import reply
from bot.keyboards.inline.order_kb import get_inline_shoes
from bot.utils.db import check_user_in_db, Order
from bot.utils.statesform import FSMCreateOrder


router = Router()
order = Order()


logging.basicConfig(level=logging.INFO,
                    format='%(filename)s -> [LINE:%(lineno)d] -> %(levelname)-8s [%(asctime)s] -> %(message)s',
                    filename='bot/logging.log',
                    filemode='w')


@router.message(F.text == '🛒Оформити замовлення')
async def place_order(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    user_in_db = await check_user_in_db(user_id=user_id)
    if user_in_db:
        await msg.answer('Введіть артикул товару:')
        await state.set_state(FSMCreateOrder.SHOES_MODEL)
    else:
        user_msg = 'Для початку давай зареєструємо твій обліковий запис.\n\n' \
                   'Щоб почати реєстрацію - натисніть\n<u><b>/registration</b></u>'
        await msg.answer(user_msg)


@router.message(FSMCreateOrder.SHOES_MODEL)
async def get_shoes_model(msg: Message, state: FSMContext) -> None:
    model = await order.check_article(msg.text)
    if not model:
        await msg.answer(f"'{msg.text}' не знайдено.")
    else:
        await msg.answer('Оберіть модель:', reply_markup=get_inline_shoes(model))

