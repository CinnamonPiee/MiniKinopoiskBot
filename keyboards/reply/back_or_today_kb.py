from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime


def back_or_today_kb():
    button1 = KeyboardButton(text=f"{datetime.date.today()}")
    button2 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
