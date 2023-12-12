from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.utils.commands import registered_users_commands
from bot.utils.db import registration_user
from bot.utils.statesform import FSMRegisterForm
from bot.keyboards.base import reply
from bot.filters.filters import RegisterUserFilter

router = Router()


@router.message(Command('registration'), RegisterUserFilter())
async def start_registration(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"<b>{msg.from_user.first_name}</b>, введіть ваше ім'я: ")
    await state.set_state(FSMRegisterForm.GET_NAME)


@router.message(FSMRegisterForm.GET_NAME)
async def get_name(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"<b>Ваше ім'я</b>: {msg.text}✅\n\n"\
                     "Далі введіть свій номер телефону або натисніть кнопку нижче⬇️:",
                     reply_markup=reply.get_phone_keyboard())
    await state.update_data(name=msg.text)
    await state.update_data(tg_id=msg.from_user.id)
    try:
        await state.update_data(username=msg.from_user.username)
    except:
        await state.update_data(username=' ')

    await state.update_data(balance=0)

    await state.set_state(FSMRegisterForm.GET_PHONE)


@router.message(FSMRegisterForm.GET_PHONE)
async def get_phone(msg: Message, state: FSMContext) -> None:
    await msg.answer('Введіть номер своєї картки для виплат💰:')
    if msg.text:
        await state.update_data(phone=msg.text)
    elif msg.contact is not None:
        await state.update_data(phone=msg.contact.phone_number)

    await state.set_state(FSMRegisterForm.GET_CARD)


@router.message(FSMRegisterForm.GET_CARD)
async def get_card(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"<b>Ваша картка</b>:\n {msg.text}✅")
    await state.update_data(bank_card=msg.text)
    context_data = await state.get_data()
    name = context_data.get('name')
    phone = context_data.get('phone')
    karta = context_data.get('bank_card')
    data_user = f"Перевірте свої дані та оберіть нижче потрібний вам пункт⏳:\n\n" \
                f"<b>Ваше ім'я:</b>\n ▪️{name}\n\n" \
                f"<b>Ваш номер телефону:</b>\n ▪️{phone}\n\n" \
                f"<b>Ваша картка для виплат:</b>\n ▪️{karta}"
    await msg.answer(data_user, reply_markup=reply.confirmation_data())

    await state.set_state(FSMRegisterForm.FINISH_REGISTER)


@router.message(FSMRegisterForm.FINISH_REGISTER)
async def finish_register(msg: Message, state: FSMContext, bot: Bot) -> None:
    if msg.text == '✅Все вірно, підтверджую реєстрацію':
        context_data = await state.get_data()
        await registration_user(context_data)
        await msg.answer('Ви успішно зареєстровані🎉', reply_markup=reply.start_keyboard())
        await registered_users_commands(bot)

    elif msg.text == '📛Є помилкові дані, почнемо заново':
        await state.clear()
        await msg.answer('Натисніть <u><b>/registration</b></u>,\nдля того, щоб розпочати заново.')
    elif msg.text == '❌Відмінити реєстрацію':
        await state.clear()
        await msg.answer('Реєстрація відмінена.', reply_markup=reply.start_keyboard())
