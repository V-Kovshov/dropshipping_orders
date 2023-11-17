from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.db import check_orders_balance, get_users_orders, get_orders_by_client_surname, check_user_in_db
from bot.utils.statesform import FSMSearchOrderFromProfile
from bot.keyboards.base import reply
from bot.keyboards.inline import user_profile_kb


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
	if all_orders:
		await msg.answer(text='Усі замовлення:', reply_markup=user_profile_kb.all_orders_kb(all_orders))
	else:
		await msg.answer(text='Ви ще не здавали замовлення☹️',
						reply_markup=reply.back_to_profile_kb())


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
	await msg.answer(
		text='Замовлення за вашим запитом:🕵🏼',
		reply_markup=user_profile_kb.found_orders_kb(found_orders))
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
