from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def choose_criteries_kb() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="Найти фильм / сериал")
    button2 = KeyboardButton(text="Рандомный фильм / сериал")
    button3 = KeyboardButton(text="Кастомный поиск")
    button4 = KeyboardButton(text="Назад")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2, button3], [button4]],
        resize_keyboard=True,
        one_time_keyboard=True, 
    )

    return keyboard
