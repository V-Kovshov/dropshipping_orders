from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from bot.utils.db import get_all_balance


router = Router()


@router.message(F.text == '👤Кабінет')
async def private_cabinet(msg: Message) -> None:
	balance = await get_all_balance(msg.from_user.id)
	await msg.answer(f'Ваш баланс: {balance}грн')
