from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_kb() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
