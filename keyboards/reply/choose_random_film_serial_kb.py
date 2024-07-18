from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def choose_random_film_serial_kb():
    button1 = KeyboardButton(text="Фильм")
    button2 = KeyboardButton(text="Сериал")
    button3 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2],
                  [button3]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard
