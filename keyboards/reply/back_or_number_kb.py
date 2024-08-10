from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_or_number_kb() -> ReplyKeyboardMarkup:
    button2 = KeyboardButton(text="Поделиться номером", request_contact=True)
    button1 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
