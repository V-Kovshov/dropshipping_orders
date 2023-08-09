from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_keyboard():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='👤Кабінет')
    kb_builder.button(text='🛒Оформити замовлення')
    kb_builder.button(text='🤝Підтримка')
    kb_builder.adjust(1, 2)

    return kb_builder.as_markup(resize_keyboard=True, input_field_placeholder='Оберіть один із варіантів', one_time_keyboard=True)


def get_phone_keyboard():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='☎️Відправити свій номер телефону', request_contact=True)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def confirmation_data():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='✅Все вірно, підтверджую реєстрацію')
    kb_builder.button(text='📛Є помилкові дані, почнемо заново')
    kb_builder.button(text='❌Відмінити реєстрацію')

    kb_builder.adjust(1, 1, 1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
