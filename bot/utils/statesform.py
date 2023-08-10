from aiogram.fsm.state import StatesGroup, State


class FSMRegisterForm(StatesGroup):
	GET_NAME = State()
	GET_PHONE = State()
	GET_CARD = State()
	FINISH_REGISTER = State()


class FSMCreateOrder(StatesGroup):
	SHOES_MODEL = State()
	SHOES_SIZE = State()
	CLIENT_NAME = State()
	CLIENT_PHONE = State()
	OTHER_DATA = State()
	POSTPAYMENT = State()
	BALANCE_PAY = State()
	SCREEN_PAYMENT = State()
