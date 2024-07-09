from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


PER_PAGE = 5


def create_pagination_kb(history, current_page, total_count):
    buttons = []

    for record in history:
        buttons.append(
            [InlineKeyboardButton(text=f"{record.film.name}", callback_data=f"film_{record.film.id}")]
        )

    total_pages = (total_count + PER_PAGE - 1) // PER_PAGE

    navigation_buttons = []
    if current_page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{current_page - 1}"))

    navigation_buttons.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="noop"))

    if current_page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{current_page + 1}"))

    buttons.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
