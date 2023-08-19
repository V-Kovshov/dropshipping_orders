import logging

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from bot.keyboards.base import reply
from bot.keyboards.inline.order_kb import get_inline_shoes, get_inline_size
# from bot.middlewares.size import GetSizeMiddleware
from bot.utils.db import check_user_in_db, Order
from bot.utils.statesform import FSMCreateOrder

router = Router()
# router.callback_query.middleware(GetSizeMiddleware())
order = Order()

logging.basicConfig(level=logging.INFO,
					format='%(filename)s -> [LINE:%(lineno)d] -> %(levelname)-8s [%(asctime)s] -> %(message)s',
					filename='bot/logging.log',
					filemode='w')


@router.message(F.text == '🛒Оформити замовлення')
async def place_order(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер перевіряє чи клінєнт зареєстрований та отримує від клієнта артикул товару

	:param msg:
	:param state:
	:return: None
	"""
	user_id = msg.from_user.id
	user_in_db = await check_user_in_db(user_id=user_id)
	if user_in_db:
		await msg.answer('📝Введіть артикул товару:')
		await state.set_state(FSMCreateOrder.CHOOSE_MODEL)
	else:
		user_msg = '🤔Для початку давай зареєструємо твій обліковий запис.\n\n' \
				   'Щоб почати реєстрацію - натисніть\n<u><b>/registration</b></u>'
		await msg.answer(user_msg)


@router.message(FSMCreateOrder.CHOOSE_MODEL)
async def search_model(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер отримує артикул товару та шукає модель в БД по артикулу

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	model = await order.check_article(msg.text)
	if not model:
		await msg.answer(f"🤷🏼‍♂️'{msg.text}' не знайдено.\nСпробуйте іншу модель.")
	else:
		await msg.answer('👠Тепер оберіть модель:', reply_markup=get_inline_shoes(model))
		await state.set_state(FSMCreateOrder.CHOOSE_SIZE)


@router.callback_query(FSMCreateOrder.CHOOSE_SIZE)
async def choose_size(call: CallbackQuery, state: FSMContext) -> None:
	"""
	Хендлер зберігає модель взуття та виводить фото моделі, опис та розміри моделі

	:param call: CallbackQuery
	:param state: FSMContext
	:return: None
	"""
	await state.update_data(model=int(call.data))

	shoes = await order.get_model(int(call.data))
	shoes_img_url = str(shoes.image.url)[1:]
	photo = FSInputFile(shoes_img_url)

	sizes = await order.get_model_sizes(model_id=int(call.data))
	await call.message.answer_photo(
		photo=photo,
		caption=f"{shoes.description}\n\n📏Оберіть потрібний розмір:",
		reply_markup=get_inline_size(sizes)
	)
	await state.set_state(FSMCreateOrder.CLIENT_NAME)
	await call.answer()


@router.callback_query(FSMCreateOrder.CLIENT_NAME)
async def get_client_name(call: CallbackQuery, state: FSMContext) -> None:
	"""
	Хендлер зберігає розмір взуття та отримує від клієнта ПІБ клієнта

	:param call:
	:param state:
	:return: None
	"""
	await state.update_data(shoes_size=int(call.data))
	await call.message.answer("🪪Введіть ПІБ клієнта:")
	await state.set_state(FSMCreateOrder.CLIENT_PHONE)
	await call.answer()


@router.message(FSMCreateOrder.CLIENT_PHONE)
async def get_client_phone(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає ПІБ клієнта та отримує від клієнта номер телефону клієнта

	:param msg:
	:param state:
	:return: None
	"""
	await state.update_data(client_name=msg.text)
	await msg.answer('📱Введіть номер телефону клієнта:')
	await state.set_state(FSMCreateOrder.OTHER_DATA)


@router.message(FSMCreateOrder.OTHER_DATA)
async def get_other_data(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає номер телефону клієнта та отримує інші дані для відправлення (місто, відділення пошти тощо)

	:param msg:
	:param state:
	:return: None
	"""
	await state.update_data(client_phone=msg.text)
	await msg.answer('📥Введіть назву населеного пункту,\nвідділення Нової пошти та інші дані за потреби:')
	await state.set_state(FSMCreateOrder.POSTPAYMENT)


@router.message(FSMCreateOrder.POSTPAYMENT)
async def get_postpayment(msg: Message, state: FSMContext) -> None:
	await state.update_data(otder_data=msg.text)
	await msg.answer('💸Введіть суму накладного платежу, якщо він є.\n\n'
					'Якщо накладного платежу немає - введіть 0 (цифра)')
	await state.set_state(FSMCreateOrder.BALANCE_PAY)


@router.message(FSMCreateOrder.BALANCE_PAY)
async def advance_from_balance(msg: Message, state: FSMContext) -> None:
	await state.update_data(postpayment=int(msg.text))
	user_id = msg.from_user.id
	available_balance = await order.get_balance(user_id)
	await msg.answer('💳Введіть суму авансу с балансу:\n\n'
					f'✅Доступний баланс: {available_balance},00грн\n\n'
					'🔜Якщо буде передоплата - введіть 0(цифра) та переходьте на наступний крок\n\n')
	await state.set_state(FSMCreateOrder.SCREEN_PAYMENT)


@router.message(FSMCreateOrder.SCREEN_PAYMENT)
async def get_screen_payment(msg: Message, state: FSMContext) -> None:
	print(msg)
