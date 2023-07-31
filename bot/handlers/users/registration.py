from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.utils.statesform import FSMRegisterForm
from bot.keyboards.base import reply

router = Router()


@router.message(Command(commands='registration'))
async def start_registration(msg: Message, state: FSMContext):
    await msg.answer(f"{msg.from_user.first_name}, введіть ваше ім'я: ")
    await state.set_state(FSMRegisterForm.GET_NAME)


@router.message(FSMRegisterForm.GET_NAME)
async def get_name(msg: Message, state: FSMContext):
    await msg.answer(f"Ваше ім'я: {msg.text}\n\n" \
                     "Далі введіть свій номер телефону або натисніть кнопку нижче",
                     reply_markup=reply.get_phone_keyboard())
    await state.update_data(name=msg.text)
    await state.set_state(FSMRegisterForm.GET_PHONE)


@router.message(FSMRegisterForm.GET_PHONE)
async def get_phone(msg: Message, state: FSMContext):
    await msg.answer('Введіть номер своєї картки для виплат')
    if msg.text:
        await state.update_data(phone=msg.text)
    elif msg.contact is not None:
        await state.update_data(phone=msg.contact.phone_number)
    await state.set_state(FSMRegisterForm.GET_CARD)


@router.message(FSMRegisterForm.GET_CARD)
async def get_card(msg: Message, state: FSMContext):
    ...
