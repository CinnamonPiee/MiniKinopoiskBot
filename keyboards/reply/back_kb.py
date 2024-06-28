from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_kb():
    button1 = KeyboardButton(text="Back")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
