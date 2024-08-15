from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def yes_no_back() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")
    button3 = KeyboardButton(text="🚫 Назад 🚫")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1, button2], [button3]],
        resize_keyboard=True,
        one_time_keyboard=True, 
    )

    return keyboard
