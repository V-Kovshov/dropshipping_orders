import logging
import os

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, File
from aiogram.fsm.context import FSMContext

from bot.keyboards.base import reply
from bot.keyboards.inline.order_kb import get_inline_shoes, get_inline_size
from bot.utils.db import check_user_in_db, Order
from bot.utils.statesform import FSMCreateOrder
from bot.utils import check


router = Router()
order = Order()

logging.basicConfig(level=logging.INFO,
					format='%(filename)s -> [LINE:%(lineno)d] -> %(levelname)-8s [%(asctime)s] -> %(message)s',
					filename='bot/logging.log',
					filemode='w')


@router.message(F.text == '🛒Оформити замовлення')
async def place_order(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер перевіряє чи клієнт зареєстрований та отримує від клієнта артикул товару.

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
	Хендлер отримує артикул товару та шукає модель в БД по артикулу.

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	model = await order.check_article(msg.text)
	if not model:
		await msg.answer(f"🤷🏼‍♂️'{msg.text}' не знайдено.\n\nСпробуйте іншу модель.")
	else:
		await msg.answer('👠Тепер оберіть модель:', reply_markup=get_inline_shoes(model))
		await state.set_state(FSMCreateOrder.CHOOSE_SIZE)


@router.callback_query(FSMCreateOrder.CHOOSE_SIZE)
async def choose_size(call: CallbackQuery, state: FSMContext) -> None:
	"""
	Хендлер зберігає модель взуття та виводить фото моделі, опис та розміри моделі.

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


@router.message(FSMCreateOrder.CHOOSE_SIZE)
async def choose_size_wrong(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер повідомляє юзеру, що потрібно обрати модель із списку запропонованих, якщо юзер ввів свій варіант.

	:param msg: Message
	:param state: FSMContext
	:return: none
	"""
	await msg.answer('Вам потрібно обрати одну з моделей вище☝🏼')
	await state.set_state(FSMCreateOrder.CHOOSE_SIZE)


@router.callback_query(FSMCreateOrder.CLIENT_NAME)
async def get_client_name(call: CallbackQuery, state: FSMContext) -> None:
	"""
	Хендлер зберігає розмір взуття та отримує від клієнта ПІБ клієнта.

	:param call: CallbackQuery
	:param state: FSMContext
	:return: None
	"""
	await state.update_data(shoes_size=int(call.data))
	await call.message.answer("🪪Введіть ПІБ клієнта:")
	await state.set_state(FSMCreateOrder.CLIENT_PHONE)
	await call.answer()


@router.message(FSMCreateOrder.CLIENT_PHONE)
async def get_client_phone(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає ПІБ клієнта та отримує від клієнта номер телефону клієнта.

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	await state.update_data(client_name=msg.text)
	await msg.answer('📱Введіть номер телефону клієнта:\n\n'
					'Наприклад "0931112233", без пробілів, "+38" тощо.')
	await state.set_state(FSMCreateOrder.OTHER_DATA)


@router.message(FSMCreateOrder.OTHER_DATA)
async def get_other_data(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає номер телефону клієнта та отримує інші дані для відправлення (місто, відділення пошти тощо).

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	if await check.check_client_phone(msg.text):
		await state.update_data(client_phone=msg.text)
		await msg.answer('📥Місто/смт/село,\nвідділення/поштомат Нової пошти, інші дані тощо:')
		await state.set_state(FSMCreateOrder.CHOICE_PAY)
	else:
		await msg.answer('Будь-ласка, введіть коректний номер телефону згідно прикладу.')
		await state.set_state(FSMCreateOrder.OTHER_DATA)


@router.message(FSMCreateOrder.CHOICE_PAY)
async def choice_pay(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає інформацію про місце доставлення та очікує від юзера тип оплати.

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	await state.update_data(other_data=msg.text)
	await msg.answer('Оберіть тип оплати (з балансу або передоплата):', reply_markup=reply.choice_pay_kb())
	await state.set_state(FSMCreateOrder.CHOSE_PAY)


@router.message(FSMCreateOrder.CHOSE_PAY, F.text.in_({'З балансу', 'По передоплаті'}))
async def chose_pay(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер визначає яка оплата (з балансу або передоплата) була обрана та очікує відповідь про тип оплати.

	:param msg: Message
	:param state: FSMContext
	:return: None
	"""
	if msg.text == 'З балансу':
		await msg.answer('🧮Накладний платіж або повна оплата?', reply_markup=reply.advance_or_full_kb())
		await state.set_state(FSMCreateOrder.BALANCE_PAY)
	elif msg.text == 'По передоплаті':
		await msg.answer('🧮Накладний платіж або повна оплата?', reply_markup=reply.advance_or_full_kb())
		await state.set_state(FSMCreateOrder.SCREEN_PAY)


@router.message(FSMCreateOrder.CHOSE_PAY)
async def chose_pay_wrong(msg: Message, state: FSMContext) -> None:
	"""
	Якщо юзер не натиснув на кнопку та ввів свій варіант.

	:param state: FSMContext
	:param msg: Message
	:return: None
	"""
	await msg.answer('🤔Вам потрібно обрати один із варіантів оплати нижче:', reply_markup=reply.choice_pay_kb())
	await state.set_state(FSMCreateOrder.CHOSE_PAY)


@router.message(FSMCreateOrder.BALANCE_PAY, F.text.in_({'Аванс з накладним платежем', 'Повна оплата'}))
async def balance_pay(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер запитує юзера тип оплати (повна або накладний).

	:param msg: Message
	:param state: FSMContext
	:return: none
	"""
	available_balance = await order.check_balance(msg.from_user.id)
	if msg.text == 'Аванс з накладним платежем':
		await msg.answer(f'✅Доступний баланс: {available_balance},00грн\n\n'
						'Введіть суму авансу:\n(Наприклад "200")')
		await state.set_state(FSMCreateOrder.BALANCE_PAY_ADVANCE)

	elif msg.text == 'Повна оплата':
		await msg.answer(f'✅Доступний баланс: {available_balance},00грн\n\n'
						'Введіть суму оплати:\n(Наприклад "1550")')
		await state.set_state(FSMCreateOrder.CHECK_ORDER_BALANCE)


@router.message(FSMCreateOrder.BALANCE_PAY)
async def balance_pay_wrong(msg: Message, state: FSMContext) -> None:
	"""
	Якщо юзер не натиснув на кнопку та ввів свій варіант.

	:param state: FSMContext
	:param msg: Message
	:return: None
	"""
	await msg.answer('🤔Вам потрібно обрати один із варіантів оплати нижче:', reply_markup=reply.advance_or_full_kb())
	await state.set_state(FSMCreateOrder.BALANCE_PAY)


@router.message(FSMCreateOrder.BALANCE_PAY_ADVANCE)
async def balance_pay_advance(msg: Message, state: FSMContext) -> None:
	"""
	Хендлер зберігає суму авансу з балансу та очікує суму накладного платежу від юзера.

	:param msg: Message
	:param state: FSMContext
	:return: none
	"""
	if await check.check_pay_sum(msg.text):
		if await order.check_balance(msg.from_user.id) < int(msg.text):
			await msg.answer(f'⛔️Не вистачає коштів на балансі.\n\n'
							'Оберіть тип оплати (з балансу або передоплата):',
							reply_markup=reply.choice_pay_kb())
			await state.set_state(FSMCreateOrder.CHOSE_PAY)
		else:
			await state.update_data(balance_advance=msg.text)
			await msg.answer('💰Введіть суму накладного платежу:\n(Наприклад "1550")')
			await state.set_state(FSMCreateOrder.CHECK_ORDER_BALANCE_ADVANCE)
	else:
		await msg.answer('Введіть коректну суму авансу згідно прикладу.')
		await state.set_state(FSMCreateOrder.BALANCE_PAY_ADVANCE)


@router.message(FSMCreateOrder.CHECK_ORDER_BALANCE_ADVANCE)
async def check_order_balance_advance(msg: Message, state: FSMContext) -> None:
	if await check.check_pay_sum(msg.text):
		if await order.check_balance(msg.from_user.id) < int(msg.text):
			await msg.answer(f'⛔️Не вистачає коштів на балансі.\n\n'
							'Оберіть тип оплати (з балансу або передоплата):',
							reply_markup=reply.choice_pay_kb())
			await state.set_state(FSMCreateOrder.CHOSE_PAY)
		else:
			await state.update_data(postpayment=msg.text)

			context_data = await state.get_data()
			model = await order.get_model(context_data.get('model'))
			size = await order.get_size(context_data.get('shoes_size'))
			client_name = context_data.get('client_name')
			client_phone = context_data.get('client_phone')
			other_data = context_data.get('other_data')
			balance_advance = context_data.get('balance_advance')
			postpayment = context_data.get('postpayment')

			await msg.answer('Давай перевіримо дані')

			data = f"▫️<b>Модель взуття:</b> {model.article}\n" \
				f"▫️<b>Розмір:</b> {size}\n"\
				f"▫️<b>ПІБ клієнта:</b> {client_name}\n" \
				f"▫️<b>Телефон клієнта:</b> {client_phone}\n" \
				f"▫️<b>Інші дані для відправки:</b> {other_data}\n" \
				f"▫️<b>Аванс:</b> {balance_advance}.00грн\n" \
				f"▫️<b>Накладний платіж:</b> {postpayment}.00грн\n"
			await msg.answer(data, reply_markup=reply.check_data_order_kb())

			await state.set_state(FSMCreateOrder.FINISH_CREATE_ORDER)
	else:
		await msg.answer('Введіть коректну суму накладного платежу згідно прикладу.')
		await state.set_state(FSMCreateOrder.CHECK_ORDER_BALANCE_ADVANCE)


@router.message(FSMCreateOrder.CHECK_ORDER_BALANCE)
async def balance_pay_full(msg: Message, state: FSMContext) -> None:
	if await check.check_pay_sum(msg.text):
		if await order.check_balance(msg.from_user.id) < int(msg.text):
			await msg.answer(f'⛔️Не вистачає коштів на балансі.\n\n'
							'Оберіть тип оплати (з балансу або передоплата):',
							reply_markup=reply.choice_pay_kb())
			await state.set_state(FSMCreateOrder.CHOSE_PAY)
		else:
			await state.update_data(pay=msg.text)

			context_data = await state.get_data()
			model = await order.get_model(context_data.get('model'))
			size = await order.get_size(context_data.get('shoes_size'))
			client_name = context_data.get('client_name')
			client_phone = context_data.get('client_phone')
			other_data = context_data.get('other_data')
			pay = context_data.get('pay')

			await msg.answer('Давай перевіримо дані')

			data = f"▫️<b>Модель взуття:</b> {model.article}\n" \
				f"▫️<b>Розмір:</b> {size}\n"\
				f"▫️<b>ПІБ клієнта:</b> {client_name}\n" \
				f"▫️<b>Телефон клієнта:</b> {client_phone}\n" \
				f"▫️<b>Інші дані для відправки:</b> {other_data}\n" \
				f"▫️<b>Аванс:</b> {pay}.00грн\n"
			await msg.answer(data, reply_markup=reply.check_data_order_kb())

			await state.set_state(FSMCreateOrder.FINISH_CREATE_ORDER)
	else:
		await msg.answer('Введіть коректну суму оплати.')
		await state.set_state(FSMCreateOrder.CHECK_ORDER_BALANCE)


@router.message(FSMCreateOrder.SCREEN_PAY, F.text.in_({'Аванс з накладним платежем', 'Повна оплата'}))
async def screen_pay(msg: Message, state: FSMContext) -> None:
	if msg.text == 'Аванс з накладним платежем':
		await msg.answer('Напишіть суму авансу та через кому суму накладного платежу:\n\n'
						'Наприклад "<b>200,1650</b>"(без будь-яких інших символів)')
		await state.set_state(FSMCreateOrder.SCREEN_PAY_ADVANCE)
	elif msg.text == 'Повна оплата':
		await msg.answer('Надішліть скрін з оплатою:\n\n'
						"Обов'язково в коментарях до оплати напишіть прізвище клієнта.")
		await state.set_state(FSMCreateOrder.SCREEN_PAY_FULL)


@router.message(FSMCreateOrder.SCREEN_PAY)
async def balance_pay_wrong(msg: Message, state: FSMContext) -> None:
	"""
	Якщо юзер не натиснув на кнопку та ввів свій варіант.

	:param state: FSMContext
	:param msg: Message
	:return: None
	"""
	await msg.answer('Вам потрібно обрати один із варіантів оплати нижче:', reply_markup=reply.advance_or_full_kb())
	await state.set_state(FSMCreateOrder.SCREEN_PAY)


@router.message(FSMCreateOrder.SCREEN_PAY_ADVANCE)
async def screen_pay_advance(msg: Message, state: FSMContext) -> None:
	await state.update_data(pay=msg.text)
	await msg.answer('Надішліть скрін з оплатою:\n\n'
					"Обов'язково в коментарях до оплати напишіть прізвище клієнта.")
	await state.set_state(FSMCreateOrder.CHECK_ORDER_SCREEN_ADVANCE)


@router.message(FSMCreateOrder.CHECK_ORDER_SCREEN_ADVANCE)
async def check_order_screen_advance(msg: Message, bot: Bot, state: FSMContext) -> None:
	# Зберігаємо скрін з оплатою від клієнта в теку під його ім'ям
	user_path = await order.get_user_name(msg.from_user.id)
	photo_id = msg.photo[-1].file_id
	photo_file = await bot.get_file(photo_id)
	photo_path = photo_file.file_path.removeprefix('photos/')
	if not os.path.exists(f'bot/media/payment/{user_path}/'):
		os.mkdir(f'bot/media/payment/{user_path}/')
	await bot.download(file=photo_id, destination=f'bot/media/payment/{user_path}/{photo_path}')
	# Перевірка даних замовлення перед оформленням
	context_data = await state.get_data()
	model = await order.get_model(context_data.get('model'))
	size = await order.get_size(context_data.get('shoes_size'))
	client_name = context_data.get('client_name')
	client_phone = context_data.get('client_phone')
	other_data = context_data.get('other_data')
	balance_advance, postpayment = context_data.get('pay').split(',')
	# postpayment = context_data.get('postpayment')
	await msg.answer('Давай перевіримо дані')

	data = f"▫️<b>Модель взуття:</b> {model.article}\n" \
		f"▫️<b>Розмір:</b> {size}\n" \
		f"▫️<b>ПІБ клієнта:</b> {client_name}\n" \
		f"▫️<b>Телефон клієнта:</b> {client_phone}\n" \
		f"▫️<b>Інші дані для відправки:</b> {other_data}\n" \
		f"▫️<b>Аванс:</b> {balance_advance}.00грн\n" \
		f"▫️<b>Накладний платіж:</b> {postpayment}.00грн\n"
	await msg.answer(data, reply_markup=reply.check_data_order_kb())

	await state.set_state(FSMCreateOrder.FINISH_CREATE_ORDER)


@router.message(FSMCreateOrder.SCREEN_PAY_FULL)
async def screen_pay_full(msg: Message, bot: Bot, state: FSMContext) -> None:
	# Зберігаємо скрін з оплатою від клієнта в теку під його ім'ям
	user_path = await order.get_user_name(msg.from_user.id)
	photo_id = msg.photo[-1].file_id
	photo_file = await bot.get_file(photo_id)
	photo_path = photo_file.file_path.removeprefix('photos/')
	if not os.path.exists(f'bot/media/payment/{user_path}/'):
		os.mkdir(f'bot/media/payment/{user_path}/')
	await bot.download(file=photo_id, destination=f'bot/media/payment/{user_path}/{photo_path}')
	# Перевірка даних замовлення перед оформленням
	context_data = await state.get_data()
	model = await order.get_model(context_data.get('model'))
	size = await order.get_size(context_data.get('shoes_size'))
	client_name = context_data.get('client_name')
	client_phone = context_data.get('client_phone')
	other_data = context_data.get('other_data')

	await msg.answer('Давай перевіримо дані')

	data = f"▫️<b>Модель взуття:</b> {model.article}\n" \
		f"▫️<b>Розмір:</b> {size}\n" \
		f"▫️<b>ПІБ клієнта:</b> {client_name}\n" \
		f"▫️<b>Телефон клієнта:</b> {client_phone}\n" \
		f"▫️<b>Інші дані для відправки:</b> {other_data}\n" \
		f"▫️<b>Аванс:</b> {model.price_opt}\n"
	await msg.answer(data, reply_markup=reply.check_data_order_kb())

	await state.set_state(FSMCreateOrder.FINISH_CREATE_ORDER)



@router.message(FSMCreateOrder.FINISH_CREATE_ORDER, F.text == 'Підтверджую')
async def finish_create_order(msg: Message, state: FSMContext) -> None:
	# TODO: зробити оформлення замовлення в БД
	await msg.answer('🌹Ваше замовлення оформлено!🌹\n\nТТН буде в посиланні на це замовлення в вашому кабінеті')
	await state.clear()


@router.message(FSMCreateOrder.FINISH_CREATE_ORDER, F.text == 'Відмінити')
async def finish_create_order(msg: Message, state: FSMContext) -> None:
	await msg.answer('Оформлення замовлення скасовано', reply_markup=reply.start_keyboard())
	await state.clear()
