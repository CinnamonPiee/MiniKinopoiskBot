from aiogram import Router, types

from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

from database.orm.film import add_film, film_exists
from database.orm.serial import add_serial, serial_exists

from keyboards.inline.create_random_pagination_kb import create_random_pagination_kb
from keyboards.reply.main_kb import main_kb

from utils.validations import (
    valid_user_and_film_id_in_history,
    valid_user_and_serial_id_in_history
)
from utils.get_film_data import get_film_data
from utils.get_serial_data import get_serial_data


router = Router(name=__name__)


@router.callback_query(lambda c: c.data and c.data.startswith("rand_page_") or c.data == "rand_main_menu")
async def change_random_page(callback_query: types.CallbackQuery, state: FSMContext):
    page = int(callback_query.data.split("_")[2]) if "rand_page_" in callback_query.data else 0
    data = await state.get_data()
    random_data = data.get("random_data", [])
    total_count = len(random_data)

    if callback_query.data == 'rand_main_menu':
        await callback_query.message.bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
        await callback_query.message.answer(
            text="Вы вернулись в главное меню.",
            reply_markup=main_kb(),
        )
        await state.clear()

    else:
        telegram_id = data["telegram_id"]
        await display_history(callback_query, random_data, total_count, page, telegram_id)


async def display_history(
        callback_query: types.CallbackQuery, 
        random_data: list, 
        total_count: int, 
        page: int, 
        telegram_id: int
    ):
    if not random_data:
        await callback_query.answer("Нет доступных данных.")
        return
    
    item = random_data[page]
    
    if item["type"] == "movie":
        (url,
         name,
         genres,
         rating,
         year,
         movie_length,
         countries,
         age_rating,
         description) = get_film_data(item)

        if await film_exists(name):
            await valid_user_and_film_id_in_history.valid_user_and_film_id_in_history(
                name, 
                telegram_id
            )

        else:
            if item["movieLength"] == None:
                movie_length = 0
            else:
                movie_length = int(item["movieLength"])

            await add_film(
                telegram_id=telegram_id,
                name=name,
                janr=genres,
                year=int(year),
                country=countries,
                movie_length=movie_length,
                description=description,
                rating=rating,
                age_rating=age_rating,
                picture=url
            )

        caption = f"{markdown.hbold(name)}\n"\
                  f"Жанры: {genres}\n"\
                  f"Рейтинг: {rating}\n"\
                  f"Год: {year}\n"\
                  f"Продолжительность фильма: {movie_length}\n"\
                  f"Страна: {countries}\n"\
                  f"Возрастной рейтинг: {age_rating}\n"\
                  f"Описание: {description}"\
                  
        keyboards = create_random_pagination_kb(page, total_count)

        try:
            await callback_query.message.edit_media(
                media=types.InputMediaPhoto(
                    media=url,
                    caption=caption,
                ),
                reply_markup=keyboards,
            )

            await callback_query.answer()

        except:
            caption = f"{markdown.hbold(name)}\n"\
                      f"Жанры: {genres}\n"\
                      f"Рейтинг: {rating}\n"\
                      f"Год: {year}\n"\
                      f"Продолжительность фильма: {movie_length}\n"\
                      f"Страна: {countries}\n"\
                      f"Возрастной рейтинг: {age_rating}\n"\
                      f"Описание: None"\

            await callback_query.message.edit_media(
                media=types.InputMediaPhoto(
                    media=url,
                    caption=caption,
                ),
                reply_markup=keyboards,
            )

            await callback_query.answer()

    elif item["type"] == "tv-series":
        (url,
         name,
         genres,
         rating,
         release_years,
         series_length,
         countries,
         age_rating,
         description) = get_serial_data(item)

        if await serial_exists(name):
            await valid_user_and_serial_id_in_history.valid_user_and_serial_id_in_history(
                name, 
                telegram_id
            )

        else:
            await add_serial(
                telegram_id=telegram_id,
                name=name,
                janr=genres,
                rating=rating,
                release_year=release_years,
                series_length=series_length,
                country=countries,
                age_rating=age_rating,
                description=description,
                picture=url
            )

        caption = f"{markdown.hbold(name)}\n"\
                  f"Жанры: {genres}\n"\
                  f"Рейтинг: {rating}\n"\
                  f"Релиз: {release_years}\n"\
                  f"Продолжительность серии: {series_length}\n"\
                  f"Страна: {countries}\n"\
                  f"Возрастной рейтинг: {age_rating}\n"\
                  f"Описание: {description}"\

        keyboards = create_random_pagination_kb(page, total_count)

        try:
            await callback_query.message.edit_media(
                media=types.InputMediaPhoto(
                    media=url,
                    caption=caption,
                ),
                reply_markup=keyboards,
            )

            await callback_query.answer()

        except:
            caption = f"{markdown.hbold(name)}\n"\
                      f"Жанры: {genres}\n"\
                      f"Рейтинг: {rating}\n"\
                      f"Релиз: {release_years}\n"\
                      f"Продолжительность серии: {series_length}\n"\
                      f"Страна: {countries}\n"\
                      f"Возрастной рейтинг: {age_rating}\n"\
                      f"Описание: None"\
                      
            await callback_query.message.edit_media(
                media=types.InputMediaPhoto(
                    media=url,
                    caption=caption,
                ),
                reply_markup=keyboards,
            )
            
            await callback_query.answer()


@router.callback_query(lambda c: c.data == "rand_noop")
async def random_noop_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
