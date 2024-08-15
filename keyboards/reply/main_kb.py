from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb() -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text="🎬 Фильмы / Сериалы 🎥")
    button2 = KeyboardButton(text="🕰 История поиска 🗒")
    button3 = KeyboardButton(text="Поддержка ⚙️")
    button4 = KeyboardButton(text="Помощь ❓")
    button5 = KeyboardButton(text="О боте ❗️")
    button6 = KeyboardButton(text="Обратная связь 📧")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1],
                  [button2],
                  [button3, button4],
                  [button5, button6]],
        resize_keyboard=True,
        one_time_keyboard=True, 
    )

    return keyboard
