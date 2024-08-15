from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def login_registration_kb() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="Вход")
    button2 = KeyboardButton(text="Регистрация")
    button3 = KeyboardButton(text="🚫 Назад 🚫")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1, button2], [button3]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
