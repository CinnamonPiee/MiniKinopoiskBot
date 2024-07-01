from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def back_or_number():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Поделиться номером телефона", request_contact=True),
        KeyboardButton(text="Назад")
    )

    return builder
