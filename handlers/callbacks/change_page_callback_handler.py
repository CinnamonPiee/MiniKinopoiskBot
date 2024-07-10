from aiogram import types, Dispatcher
from database.orm.user import check_user_id_by_telegram_id, get_user_film_history, get_user_serial_history
from keyboards.inline.create_pagination_kb import create_pagination_kb
from keyboards.reply.main_kb import main_kb
from utils.choice_film_serial_or_all import ChoiceFilmSerialOrAll


PER_PAGE = 1
dp = Dispatcher()


@dp.callback_query(lambda c: c.data and c.data.startswith('page_') or c.data == 'main_menu')
async def change_page_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()

    page = int(callback_query.data.split('_')[1]) if callback_query.data.startswith('page_') else 0
    telegram_id = callback_query.from_user.id
    user_id = await check_user_id_by_telegram_id(int(telegram_id))

    if ChoiceFilmSerialOrAll.choice == "Фильмы":
        if user_id:
            history, total_count = await get_user_film_history(user_id, page, PER_PAGE)
            if history:
                print(f"-------{history[0].film}")
                film = history[0].film
                keyboards = create_pagination_kb(page, total_count)
                if callback_query.data == 'main_menu':
                    await callback_query.message.answer(
                        text="Вы вернулись в главное меню.",
                        reply_markup=main_kb(),
                    )
                else:
                    await callback_query.message.edit_media(
                        media=types.InputMediaPhoto(
                            media=film.picture,
                            caption=f"{film.name}\n"
                                    f"Жанры: {film.janr}\n"
                                    f"Рейтинг: {film.rating}\n"
                                    f"Год: {film.year}\n"
                                    f"Продолжительность фильма: {film.movie_length}\n"
                                    f"Страна: {film.country}\n"
                                    f"Возрастной рейтинг: {film.age_rating}\n"
                                    f"Описание: {film.description}",
                        ),
                        reply_markup=keyboards
                    )

    elif ChoiceFilmSerialOrAll.choice == "Сериалы":
        if user_id:
            history, total_count = await get_user_film_history(user_id, page, PER_PAGE)
            if history:
                serial = history[0].serial
                keyboards = create_pagination_kb(page, total_count)
                if callback_query.data == 'main_menu':
                    await callback_query.message.answer(
                        text="Вы вернулись в главное меню.",
                        reply_markup=main_kb(),
                    )
                else:
                    await callback_query.message.edit_media(
                        media=types.InputMediaPhoto(
                            media=serial.picture,
                            caption=f"{serial.name}\n"
                                    f"Жанры: {serial.janr}\n"
                                    f"Рейтинг: {serial.rating}\n"
                                    f"Релиз: {serial.release_year}\n"
                                    f"Продолжительность серии: {serial.series_length}\n"
                                    f"Страна: {serial.country}\n"
                                    f"Возрастной рейтинг: {serial.age_rating}\n"
                                    f"Описание: {serial.description}",
                        ),
                        reply_markup=keyboards
                    )
