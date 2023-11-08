from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup


def start_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Кабінет🏛')
    kb_builder.button(text='Оформити замовлення🛒')
    kb_builder.button(text='Підтримка🤝')
    kb_builder.adjust(1, 2)

    return kb_builder.as_markup(resize_keyboard=True, input_field_placeholder='Оберіть один із варіантів', one_time_keyboard=True)


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='☎️Відправити свій номер телефону', request_contact=True)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def confirmation_data() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='✅Все вірно, підтверджую реєстрацію')
    kb_builder.button(text='📛Є помилкові дані, почнемо заново')
    kb_builder.button(text='❌Відмінити реєстрацію')

    kb_builder.adjust(1, 1, 1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def choice_pay_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='З балансу')
    kb_builder.button(text='По передоплаті')

    kb_builder.adjust(1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                input_field_placeholder='Баланс або передоплата')


def advance_or_full_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Аванс з накладним платежем')
    kb_builder.button(text='Повна оплата')

    kb_builder.adjust(1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                input_field_placeholder='Аванс або повна оплата')


def check_data_order_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Підтверджую')
    kb_builder.button(text='Відмінити')

    kb_builder.adjust(1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                input_field_placeholder='Перевірка даних')


def cancel_order() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Відмінити замовлення')

    kb_builder.adjust(1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def profile_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Мій баланс💰')
    kb_builder.button(text='Мої замовлення🛍')
    kb_builder.button(text='Пошук замовлення🔍')
    kb_builder.button(text='Допомога⚙️')

    kb_builder.adjust(2)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def back_to_profile_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Назад в кабінет🏛')

    kb_builder.adjust(1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
