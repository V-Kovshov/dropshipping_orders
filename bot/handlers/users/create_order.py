from aiogram import Router, Bot, F
from aiogram.types import Message

from bot.keyboards.base import reply
from bot.utils.db import check_user_in_db


router = Router()


@router.message(F.text == '🛒Оформити замовлення')
async def place_order(msg: Message, bot: Bot):
	user_id = msg.from_user.id
	user_in_db = await check_user_in_db(user_id=user_id)
	if user_in_db:
		await msg.answer(f"Ви вже зареєстровані🧐", reply_markup=reply.start_keyboard())
	else:
		user_msg = 'Для початку давай зареєструємо твій обліковий запис.\n\n' \
				'Щоб почати реєстрацію - натисніть\n<u><b>/registration</b></u>'
		await msg.answer(user_msg)
