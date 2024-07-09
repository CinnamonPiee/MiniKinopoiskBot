from aiogram import types, Router
from database.orm.user import check_user_by_telegram_id, get_user_film_history
from keyboards.inline.create_pagination_kb import create_pagination_kb
from main import dp

router = Router(name=__name__)
PER_PAGE = 5


@router.callback_query_handler(lambda c: c.data.startswith('page_'))
async def change_page_callback_handler(callback_query: types.CallbackQuery):
    current_page = int(callback_query.data.split('_')[1])
    telegram_id = callback_query.from_user.id
    user_id = await check_user_by_telegram_id(telegram_id)
    history, total_count = await get_user_film_history(user_id, current_page, PER_PAGE)
    keyboards = await create_pagination_kb(history, current_page, total_count)

    if history:
        for record in history:
            film = record.film
            await callback_query.message.edit_media(
                types.InputMediaPhoto(
                    media=film.picture,
                    caption=f"{film.name}\n"
                            f"Жанры: {film.janr}\n"
                            f"Рейтинг: {film.rating}\n"
                            f"Год: {film.year}\n"
                            f"Продолжительность фильма: {film.movie_length}\n"
                            f"Страна: {film.country}\n"
                            f"Возрастной рейтинг: {film.age_rating}\n"
                            f"Описание: {film.description}"
                ),
                reply_markup=keyboards
            )
    else:
        await callback_query.message.edit_text("История поиска пуста.", reply_markup=keyboards)