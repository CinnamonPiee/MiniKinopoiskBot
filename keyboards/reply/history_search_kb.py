from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def history_search_kb():
    button1 = KeyboardButton(text="Фильмы и сериалы")
    button2 = KeyboardButton(text="Сериалы")
    button3 = KeyboardButton(text="Фильмы")
    button4 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1],
                  [button2, button3],
                  [button4]],
        resize_keyboard=True,
        one_time_keyboard=True,
        )

    return keyboard