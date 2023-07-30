from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.utils.statesform import FSMRegisterForm

router = Router()


@router.message(Command(commands='registration'))
async def start_registration(msg: Message, state: FSMContext):
    await msg.answer(f"{msg.from_user.first_name}, введіть ваше ім'я: ")
    await state.set_state(FSMRegisterForm.GET_NAME)


@router.message(FSMRegisterForm.GET_NAME)
async def get_name(msg: Message, state: FSMContext):
    await msg.answer(f"Ваше ім'я: {msg.text}\n\n" \
                     "Далі введіть свій номер телефону або натисніть кнопку нижче")
