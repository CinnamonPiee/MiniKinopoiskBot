from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_custom_pagination_kb import create_custom_pagination_kb

from utils.validations.valid_user_and_film_id_in_history import valid_user_and_film_id_in_history
from utils.validations.valid_user_and_serial_id_in_history import valid_user_and_serial_id_in_history
from utils.validations.valid_series_length import valid_series_length
from utils.get_serial_data import get_serial_data
from utils.get_film_data import get_film_data

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from database.orm.serial import add_serial, serial_exists
from database.orm.film import add_film, film_exists


router = Router(name=__name__)


@router.message(CustomSearching.series_length, F.text == "Назад")
async def custom_searching_series_length_back(message: Message, state: FSMContext):
    data = state.get_data()

    if data["type_choice"] == "tv-series":
        await state.set_state(CustomSearching.country)
        await message.answer(
            text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
                "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
                "учитываться.",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == None:
        await state.set_data(CustomSearching.movie_length)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(CustomSearching.series_length, 
    F.text == "Пропустить" or F.text.cast(valid_series_length).as_("series_length"))
async def custom_searching_series_length_skip(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        await state.update_data(series_length=None)
    else:
        await state.update_data(series_length=message.text)

    data = state.get_data()

    if data["type_choice"] == "tv-series":
        custom_data = []

        for _ in range(int(data["count"])):
            some_data = random_custom_movie_serial_search(
                type_choice=data["type_choice"],
                year=data["year"],
                rating=data["rating"],
                age_rating=data["age_rating"],
                movie_length=data["movie_length"],
                series_length=data["series_length"],
                janr=data["janr"],
                country=data["country"]
            )

            if isinstance(some_data, dict):
                custom_data.append(some_data)
            elif isinstance(some_data, str):
                await message.answer(
                    text="Сервис временно не доступен, попробуйте позже!"
                )
                await state.clear()
                break

        if custom_data:
            await state.update_data(
                custom_data=custom_data,
                page=0, 
                telegram_id=message.from_user.id
            )

        item = custom_data[0]
        page = 0
        total_count = len(custom_data)
        keyboards = create_custom_pagination_kb(page, total_count)

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
            await valid_user_and_serial_id_in_history(name, telegram_id=message.from_user.id)

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

        caption = f"{markdown.hbold(name)}\n"\
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

    elif data["type_choice"] == None:
        await state.set_data(movie_length=None)
        await state.set_data(series_length=None)

        custom_data = []

        for _ in range(int(data["count"])):
            some_data = random_custom_movie_serial_search(
                type_choice=data["type_choice"],
                year=data["year"],
                rating=data["rating"],
                age_rating=data["age_rating"],
                movie_length=data["movie_length"],
                series_length=data["series_length"],
                janr=data["janr"],
                country=data["country"]
            )

            if isinstance(some_data, dict):
                custom_data.append(some_data)
            elif isinstance(some_data, str):
                await message.answer(
                    text="Сервис временно не доступен, попробуйте позже!"
                )
                await state.clear()
                break

        if custom_data:
            await state.update_data(
                random_data=custom_data,
                page=0,
                telegram_id=message.from_user.id
            )

        item = custom_data[0]
        page = 0
        total_count = len(custom_data)
        keyboards = create_custom_pagination_kb(page, total_count)

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
                await valid_user_and_film_id_in_history(name, telegram_id=message.from_user.id)

            else:
                await add_film(
                    telegram_id=message.from_user.id,
                    name=name,
                    janr=genres,
                    year=int(year),
                    country=countries,
                    movie_length=0 if item["movieLength"] == None else int(
                        item["movieLength"]),
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
                await valid_user_and_serial_id_in_history(name, telegram_id=message.from_user.id)

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

            caption = f"{markdown.hbold(name)}\n"\
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


@router.message(CustomSearching.series_length)
async def custom_searching_series_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность серии которую хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
