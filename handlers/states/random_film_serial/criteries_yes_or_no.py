from aiogram import Router, F

from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_kb import back_kb
from keyboards.reply.yes_no_back import yes_no_back
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_random_pagination_kb import create_random_pagination_kb

from database.orm.film import add_film, film_exists
from database.orm.serial import add_serial, serial_exists

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from utils.validations import (
    valid_user_and_film_id_in_history,
    valid_user_and_serial_id_in_history
)
from utils.get_film_data import get_film_data
from utils.get_serial_data import get_serial_data



router = Router(name=__name__)
PER_PAGE = 1


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "🚫 Назад 🚫")
async def random_film_serial_criteries_yes_or_no_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.count)
    await message.answer(
        text="Укажите количество которое вы хотите получить.",
        reply_markup=back_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "❎ Нет ❎")
async def random_film_serial_criteries_yer_or_no(message: Message, state: FSMContext):
    data = await state.get_data()
    random_data = []

    for _ in range(int(data["count"])):
        some_data = random_custom_movie_serial_search(type_choice=data["type_choice"])
        
        if isinstance(some_data, dict):
            random_data.append(some_data)
        elif isinstance(some_data, str):
            await message.answer(
                text=some_data
            )

            await state.clear()
            break

    if random_data:
        await state.update_data(random_data=random_data, page=0, telegram_id=message.from_user.id)

    item = random_data[0]
    page = 0
    total_count = len(random_data)
    keyboards = create_random_pagination_kb(page, total_count)

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
            await valid_user_and_film_id_in_history(
                name, 
                telegram_id=message.from_user.id
            )

        else:
            await add_film(
                telegram_id=message.from_user.id,
                name=name,
                janr=genres,
                year=int(year),
                country=countries,
                movie_length=0 if item["movieLength"] == None else int(item["movieLength"]),
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
        
        try:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=url,
                caption=caption,
                reply_markup=keyboards,
            )
            
        except:
            caption = f"{markdown.hbold(name)}\n"\
                      f"Жанры: {genres}\n"\
                      f"Рейтинг: {rating}\n"\
                      f"Год: {year}\n"\
                      f"Продолжительность фильма: {movie_length}\n"\
                      f"Страна: {countries}\n"\
                      f"Возрастной рейтинг: {age_rating}\n"\
                      f"Описание: None"
                      
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=url,
                caption=caption,
                reply_markup=keyboards,
            )

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
            await valid_user_and_serial_id_in_history(
                name, 
                telegram_id=message.from_user.id
            )

        else:
            await add_serial(
                telegram_id=message.from_user.id,
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

        caption=f"{markdown.hbold(name)}\n"\
                f"Жанры: {genres}\n"\
                f"Рейтинг: {rating}\n"\
                f"Релиз: {release_years}\n"\
                f"Продолжительность серии: {series_length}\n"\
                f"Страна: {countries}\n"\
                f"Возрастной рейтинг: {age_rating}\n"\
                f"Описание: {description}"\

        try:        
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=url,
                caption=caption,
                reply_markup=keyboards,
            )

        except:
            caption = f"{markdown.hbold(name)}\n"\
                      f"Жанры: {genres}\n"\
                      f"Рейтинг: {rating}\n"\
                      f"Релиз: {release_years}\n"\
                      f"Продолжительность серии: {series_length}\n"\
                      f"Страна: {countries}\n"\
                      f"Возрастной рейтинг: {age_rating}\n"\
                      f"Описание: {description}"\
                      
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=url,
                caption=caption,
                reply_markup=keyboards,
            )


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "✅ Да ✅")
async def random_film_serial_criteries_yes_or_no(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.year)
    await message.answer(
        text="Напишите год или отрывок за который хотите\n"
             "осуществить поиск, например (2016, 2008-2010).\n"
             "Максимальный - 2024.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no)
async def random_film_serial_criteries_yes_or_no_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔, выберите ,пожалуйста,\n"
             "хотите ли вы сделать рандомный поиск более подробным?",
        reply_markup=yes_no_back(),
    )
