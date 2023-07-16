from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_keyboard():
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Кабінет')
    kb_builder.button(text='Оформити замовлення')
    kb_builder.button(text='Підтримка')
    kb_builder.adjust(1, 2)

    return kb_builder.as_markup(resize_keyboard=True, input_field_placeholder='Просто натисни на одну з кнопок')