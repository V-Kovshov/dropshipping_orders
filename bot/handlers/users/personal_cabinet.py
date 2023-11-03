from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.db import check_orders_balance, get_users_orders, get_orders_by_client_surname
from bot.utils.statesform import FSMSearchOrder
from bot.keyboards.base import reply
from bot.keyboards.inline import user_profile_kb


router = Router()


@router.message(F.text == '👤Кабінет')
async def private_cabinet(msg: Message) -> None:
	await msg.answer(text='Користуйся кнопками👇🏼', reply_markup=reply.kb_profile())


@router.message(F.text == 'Мій баланс')
async def my_balance(msg: Message) -> None:
	balance = await check_orders_balance(msg.from_user.id)
	await msg.answer(f'Ваш баланс: {balance}грн')


@router.message(F.text == 'Мої замовлення')
async def my_orders(msg: Message) -> None:
	user_id = msg.from_user.id
	all_orders = await get_users_orders(user_id)
	await msg.answer(text='Усі замовлення:', reply_markup=user_profile_kb.all_orders_kb(all_orders))


@router.message(F.text == 'Пошук замовлення')
async def search_order(msg: Message, state: FSMContext) -> None:
	await msg.answer(text='Введіть прізвище клієнта:')
	await state.set_state(FSMSearchOrder.SURNAME_CLIENT)


@router.message(FSMSearchOrder.SURNAME_CLIENT)
async def get_surname_client(msg: Message, state: FSMContext) -> None:
	user_id = msg.from_user.id
	surname_client = msg.text
	found_orders = await get_orders_by_client_surname(user_id, surname_client)
