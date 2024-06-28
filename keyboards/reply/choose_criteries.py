from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def choose_criteries_kb():
    button1 = KeyboardButton(text="Find film / serial")
    button2 = KeyboardButton(text="Random film / serial")
    button3 = KeyboardButton(text="Low coast film / serial")
    button4 = KeyboardButton(text="Height coast film / serial")
    button5 = KeyboardButton(text="Custom searching")
    button6 = KeyboardButton(text="Back")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2],
                  [button3], [button4],
                  [button5], [button6]],
        resize_keyboard=True,
        one_time_keyboard=True, )

    return keyboard
