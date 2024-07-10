from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PER_PAGE = 1


def create_pagination_kb(page, total_count):
    buttons = []
    main_menu_button = [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]

    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))

    inactive_text = f"{page + 1}/{(total_count + PER_PAGE - 1) // PER_PAGE}"
    buttons.append(InlineKeyboardButton(text=inactive_text, callback_data="inactive_button"))

    if (page + 1) * PER_PAGE < total_count:
        buttons.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"page_{page + 1}"))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons, main_menu_button])

    return keyboard
