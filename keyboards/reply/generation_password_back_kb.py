from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generation_password_back_kb() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="Сгенерировать пароль")
    button2 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
