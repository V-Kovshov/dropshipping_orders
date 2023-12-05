from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asgiref.sync import sync_to_async

from bot.utils.db import (check_orders_balance, get_users_orders, get_orders_by_client_surname, check_user_in_db,
						  get_order_info)
from bot.utils.statesform import FSMSearchOrderFromProfile
from bot.utils.nova_post_api import get_status_parcel
from bot.keyboards.base import reply
from bot.keyboards.inline import user_profile_kb
from bot.models import OrderTG

from contextlib import suppress
from math import ceil


router = Router()


@router.message(F.text == 'Кабінет🏛')
async def private_cabinet(msg: Message) -> None:
	user_id = msg.from_user.id
	user_in_db = await check_user_in_db(user_id=user_id)
	if user_in_db:
		await msg.answer(text='Користуйся кнопками👇🏼', reply_markup=reply.profile_kb())
	else:
		user_msg = '🤔Для початку давай зареєструємо твій обліковий запис.\n\n' \
				'Щоб почати реєстрацію - натисніть\n<u><b>/registration</b></u>'
		await msg.answer(user_msg, reply_markup=reply.start_keyboard())


@router.message(F.text == 'Мій баланс💰')
async def my_balance(msg: Message) -> None:
	balance = await check_orders_balance(msg.from_user.id)
	await msg.answer(f'Ваш баланс: {balance}грн', reply_markup=reply.back_to_profile_kb())


@router.message(F.text == 'Мої замовлення🛍')
async def my_orders(msg: Message) -> None:
	user_id = msg.from_user.id
	all_orders = await get_users_orders(user_id)
	total_pages = ceil(len(all_orders) / 10)

	if all_orders:
		if len(all_orders) > 10:
			await msg.answer(text='Ось що ми знайшли:🕵🏼', reply_markup=user_profile_kb.all_orders_kb(all_orders[:10], total_pages))
		else:
			await msg.answer(text='Ось що ми знайшли:🕵🏼', reply_markup=user_profile_kb.all_orders_kb(all_orders, total_pages))
	else:
		await msg.answer(text='Ви ще не здавали замовлення☹️',
						reply_markup=reply.back_to_profile_kb())


@router.callback_query(user_profile_kb.PaginationCallbackFactory.filter(F.action.in_(['prev', 'next'])))
async def paginator_handler(call: CallbackQuery, callback_data: user_profile_kb.PaginationCallbackFactory) -> None:
	user_id = call.from_user.id
	all_orders = await get_users_orders(user_id)
	total_pages = ceil(len(all_orders) / 10)

	# Текущая страница
	page_num = int(callback_data.page)

	if callback_data.action == 'prev':
		page = page_num - 1 if page_num > 1 else 1
	if callback_data.action == 'next':
		page = page_num + 1 if page_num < total_pages else page_num

	if page == 1:
		with suppress(TelegramBadRequest):
			await call.message.edit_text(
				text='Ось що ми знайшли:🕵🏼',
				reply_markup=user_profile_kb.all_orders_kb(all_orders[:10], total_pages, page)
			)
	else:
		start = (page * 10) - 10
		end = start + 10
		with suppress(TelegramBadRequest):
			await call.message.edit_text(
				text='Ось що ми знайшли:🕵🏼',
				reply_markup=user_profile_kb.all_orders_kb(all_orders[start:end], total_pages, page)
			)
	await call.answer()


@router.callback_query(F.data == 'back')
async def back_btn(call: CallbackQuery) -> None:
	await call.message.answer('Користуйся кнопками👇🏼', reply_markup=reply.profile_kb())
	await call.answer()


@router.message(F.text == 'Пошук замовлення🔍')
async def search_order(msg: Message, state: FSMContext) -> None:
	user_id = msg.from_user.id
	all_orders = await get_users_orders(user_id)
	if all_orders:
		await msg.answer(text='Введіть прізвище клієнта:')
		await state.set_state(FSMSearchOrderFromProfile.SURNAME_CLIENT)
	else:
		await msg.answer(text='Ви ще не здавали замовлення☹️',
						reply_markup=reply.back_to_profile_kb())
		await state.clear()


@router.message(FSMSearchOrderFromProfile.SURNAME_CLIENT)
async def get_surname_client(msg: Message, state: FSMContext) -> None:
	user_id = msg.from_user.id
	surname_client = msg.text
	found_orders = await get_orders_by_client_surname(user_id, surname_client)
	total_orders = ceil(len(found_orders) / 10)
	if not found_orders:
		await msg.answer('Нажаль, ми нічого не знайшли🤷🏼‍♀️', reply_markup=reply.back_to_profile_kb())
	elif len(found_orders) > 10:
		await msg.answer(
			text='Ось що ми знайшли:🕵🏼',
			reply_markup=user_profile_kb.all_orders_kb(found_orders[:10], total_orders))
	else:
		await msg.answer(
			text='Ось що ми знайшли:🕵🏼',
			reply_markup=user_profile_kb.all_orders_kb(found_orders, total_orders))
	await state.clear()


@router.message(F.text == 'Допомога⚙️')
async def help_user(msg: Message) -> None:
	await msg.answer(f'В нас самих іноді виникають питання до самих себе🤷🏼‍♀️\n'
					f'Але ви завжди можете звернутися до\n'
					f'нашого менеджера: @test_name🔮',
					reply_markup=reply.back_to_profile_kb())


@router.message(F.text == 'Назад в кабінет🏛')
async def back_to_profile(msg: Message):
	await private_cabinet(msg)


@router.message(F.text == 'Назад на головну🏠')
async def back_to_start(msg: Message) -> None:
	await msg.answer(text='Ви повернулися на головну сторінку👇🏼', reply_markup=reply.start_keyboard())


@router.callback_query(F.data.startswith('ord_'))
async def order_information(call: CallbackQuery) -> None:
	order_context = await get_order_info(call.data)
	photo = order_context['photo']
	order_info = order_context['order_info']
	client_info = order_context['client_info']
	order_status = order_context['order_status']
	await call.message.answer_photo(
		photo=photo,
		caption=f"{order_info}"
				f"{client_info}"
				f"{order_status}",
		reply_markup=user_profile_kb.back_btn()
	)
	await call.answer()
