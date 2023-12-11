from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asgiref.sync import sync_to_async

from bot.utils.db import (check_orders_balance, get_users_orders, get_orders_by_client_surname, check_user_in_db,
						get_order_info, CreateOrder as Order, get_availability)
from bot.utils.statesform import FSMSearchOrderFromProfile, FSMCheckAvailable
from bot.utils.nova_post_api import get_status_parcel
from bot.keyboards.base import reply
from bot.keyboards.inline import user_profile_kb, order_kb
from bot.models import OrderTG

from contextlib import suppress
from math import ceil


router = Router()


@router.message(F.text == 'Кабінет🏛')
@router.message(Command('profile'))
async def private_cabinet(msg: Message) -> None:
	user_id = msg.chat.id
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
@router.message(F.text == 'Підтримка🤝')
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


@router.message(Command('check_availability'))
async def check_availability(msg: Message, state: FSMContext) -> None:
	await msg.answer('📝Введіть артикул товару:')
	await state.set_state(FSMCheckAvailable.SEARCH_MODEL)


@router.message(FSMCheckAvailable.SEARCH_MODEL)
async def search_model(msg: Message, state: FSMContext) -> None:
	model = await Order.check_article(msg.text)
	if not model:
		await msg.answer(f"🤷🏼‍♂️'{msg.text}' не знайдено.\n\nСпробуйте іншу модель.")
	else:
		await msg.answer('👠Тепер оберіть модель:', reply_markup=user_profile_kb.shoes_inline_kb(model))
		await state.set_state(FSMCheckAvailable.CHOOSE_MODEL)


@router.callback_query(FSMCheckAvailable.CHOOSE_MODEL)
async def choose_model(call: CallbackQuery, state: FSMContext) -> None:
	if call.data.isdigit():
		shoes = await Order.get_model(int(call.data))
		sizes = await Order.get_model_sizes(int(call.data))
		await state.update_data(model_id=int(call.data))
	elif call.data == 'back_to_availability':
		await check_availability(call.message, state)
		await call.answer()
		return

	caption = await get_availability(sizes)

	shoes_model_img = str(shoes.image.url)[1:]
	photo = FSInputFile(shoes_model_img)

	await call.message.answer_photo(
		photo=photo,
		caption=f"{shoes.description}\n\n{caption}",
		reply_markup=user_profile_kb.size_inline_kb()
	)

	await state.clear()
	await call.answer()


@router.callback_query(F.data == 'back_to_availability')
async def back_to_availability(call: CallbackQuery, state: FSMContext) -> None:
	await check_availability(call.message, state)
	await call.answer()


@router.callback_query(F.data == 'back_to_main')
async def back_to_main(call: CallbackQuery, state: FSMContext) -> None:
	await private_cabinet(call.message)
	await state.clear()
	await call.answer()


@router.message(Command('requisites'))
async def get_requisites(msg: Message) -> None:
	data = "🔺<b>Реквізити</b>🔺\n" \
		"<b>Установа банку:</b> ПриватБанк\n\n"\
		"<b>МФО банку:</b> 305299\n\n" \
		"<b>Одержувач платежу:</b>\n" \
		"ФОП ДЕМКІВ АЛІНА РУСЛАНІВНА\n\n" \
		"<b>IBAN:</b>\nUA513515330000026007052157707\n\n" \
		"<b>Рахунок отримувача:</b>\n26007052157707\n\n" \
		"<b>РНУКПН одержувача:</b>\n3260704780\n\n" \
		"<b>Призначення платежу:</b>\nОплата за товар і ПРІЗВИЩЕ КЛІЄНТА\n\n" \
		"💌<b>Зв'язатися з менеджером:</b>\n@roza_shoes_drop"
	await msg.answer(data, reply_markup=reply.start_keyboard())
