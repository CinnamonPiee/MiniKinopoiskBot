from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_custom_pagination_kb import create_custom_pagination_kb
from keyboards.reply.main_kb import main_kb

from utils.validations.valid_movie_length import valid_movie_length
from utils.validations.valid_user_and_film_id_in_history import valid_user_and_film_id_in_history
from utils.get_film_data import get_film_data

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from database.orm.film import add_film, film_exists


router = Router(name=__name__)


@router.message(CustomSearching.movie_length, F.text == "🚫 Назад 🚫")
async def custom_searching_movie_length_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.country)
    await message.answer(
        text="Напишите страну(ы), если хотите несколько старн, то\n"
             "напишите их через пробел, например\n"
             "(США, Индия Канада).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.movie_length, F.text == "⏩ Пропустить ⏩")
async def custom_searching_movie_length(message: Message, state: FSMContext):
    await state.update_data(movie_length=None)

    data = await state.get_data()

    if data["type_choice"] == "movie":

        custom_data = []

        for _ in range(int(data["count"])):
            some_data = random_custom_movie_serial_search(
                type_choice=data["type_choice"],
                year=data["year"],
                rating=data["rating"],
                age_rating=data["age_rating"],
                movie_length=data["movie_length"],
                series_length=None,
                janr=data["janr"],
                country=data["country"]
            )

            if isinstance(some_data, dict):
                custom_data.append(some_data)
            elif isinstance(some_data, str):
                await message.answer(
                    text=some_data,
                    reply_markup=main_kb(),
                )

                await state.clear()
                break

        await state.update_data(custom_data=custom_data, page=0, telegram_id=message.from_user.id)

        item = custom_data[0]
        page = 0
        total_count = len(custom_data)
        keyboards = create_custom_pagination_kb(page, total_count)

        url, name, genres, rating, year, movie_length, countries, age_rating, description = get_film_data(item)

        if await film_exists(name):
            await valid_user_and_film_id_in_history(name, telegram_id=message.from_user.id)

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

    elif data["type_choice"] == None:
        await state.set_state(CustomSearching.series_length)
        await message.answer(
            text="Напишите продолжительность серии или отрывок за который\n"
                 "хотите осуществить поиск, например\n"
                 "(40, 30-60).\n"
                 "Минимальная - 5\n"
                 "Максимальная - 200",
            reply_markup=back_or_skip_kb(),
        )


@router.message(CustomSearching.movie_length, F.text.cast(valid_movie_length).as_("movie_length"))
async def custom_searching_movie_length(message: Message, state: FSMContext):
    await state.update_data(movie_length=message.text)

    data = await state.get_data()

    if data["type_choice"] == "movie":

        custom_data = []

        for _ in range(int(data["count"])):
            some_data = random_custom_movie_serial_search(
                type_choice=data["type_choice"],
                year=data["year"],
                rating=data["rating"],
                age_rating=data["age_rating"],
                movie_length=data["movie_length"],
                janr=data["janr"],
                country=data["country"]
            )

            if isinstance(some_data, dict):
                custom_data.append(some_data)
            elif isinstance(some_data, str):
                await message.answer(
                    text=some_data,
                    reply_markup=main_kb(),
                )
                await state.clear()
                break

        await state.update_data(custom_data=custom_data, page=0, telegram_id=message.from_user.id)

        item = custom_data[0]
        page = 0
        total_count = len(custom_data)
        keyboards = create_custom_pagination_kb(page, total_count)

        url, name, genres, rating, year, movie_length, countries, age_rating, description = get_film_data(item)

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

    elif data["type_choice"] == None:
        await state.set_state(CustomSearching.series_length)
        await message.answer(
            text="Напишите продолжительность серии или отрывок за который\n"
                 "хотите осуществить поиск, например\n"
                 "(40, 30-60).\n"
                 "Минимальная - 5\n"
                 "Максимальная - 200",
            reply_markup=back_or_skip_kb(),
        )


@router.message(CustomSearching.movie_length)
async def custom_searching_movie_length_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы написали\n"
             "продолжительность фильма который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
