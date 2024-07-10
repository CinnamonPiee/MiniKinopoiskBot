from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PER_PAGE = 1


def create_pagination_kb(page, total_count):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))
    if (page + 1) * PER_PAGE < total_count:
        buttons.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"page_{page + 1}"))

    # Создаем InlineKeyboardMarkup с параметром inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

    return keyboard
