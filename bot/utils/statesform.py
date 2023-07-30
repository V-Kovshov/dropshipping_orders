from aiogram.fsm.state import StatesGroup, State


class FSMRegisterForm(StatesGroup):
	GET_NAME = State()
	GET_PHONE = State()
	GET_CARD = State()
