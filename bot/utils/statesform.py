from aiogram.fsm.state import StatesGroup, State


class FSMRegisterForm(StatesGroup):
	GET_NAME = State()
	GET_PHONE = State()
	GET_CARD = State()
	FINISH_REGISTER = State()


class FSMCreateOrder(StatesGroup):
	CHOOSE_MODEL = State()
	CHOOSE_SIZE = State()
	CLIENT_NAME = State()
	CLIENT_PHONE = State()
	OTHER_DATA = State()
	CHOICE_PAY = State()
	CHOSE_PAY = State()
	BALANCE_PAY = State()
	BALANCE_PAY_ADVANCE = State()
	CHECK_ORDER_BALANCE_ADVANCE = State()
	CHECK_ORDER_BALANCE = State()
	SCREEN_PAY = State()
	SCREEN_PAY_ADVANCE = State()
	SCREEN_PAY_FULL = State()
	CHECK_ORDER_SCREEN_ADVANCE = State()
	CHECK_ORDER_SCREEN = State()
	FINISH_BALANCE_ADVANCE = State()
	FINISH_BALANCE = State()
	FINISH_PAYFULL_ADVANCE = State()
	FINISH_PAYFULL = State()
