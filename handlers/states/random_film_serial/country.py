from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_random_pagination_kb import create_random_pagination_kb
from keyboards.reply.main_kb import main_kb

from utils.validations.valid_user_and_film_id_in_history import valid_user_and_film_id_in_history
from utils.validations.valid_user_and_serial_id_in_history import valid_user_and_serial_id_in_history
from utils.validations.valid_country import valid_country

from utils.get_film_data import get_film_data
from utils.get_serial_data import get_serial_data

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from database.orm.film import add_film, film_exists
from database.orm.serial import add_serial, serial_exists


router = Router(name=__name__)


@router.message(RandomFilmSerial.country, F.text == "🚫 Назад 🚫")
async def random_film_serial_country_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите жанр(ы), если хотите несколько жанров,\n"
             "то напишите их через пробел, например\n"
             "(боевик, драма комедия).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.country, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_country_skip(message: Message, state: FSMContext):
    await state.update_data(country=None)

    data = await state.get_data()
    random_data = []

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
            random_data.append(dict(some_data))
        elif isinstance(some_data, str):
            await message.answer(
                text=some_data,
                reply_markup=main_kb(),
            )
            await state.clear()
            break

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


@router.message(RandomFilmSerial.country, F.text.cast(valid_country).as_("country"))
async def random_film_serial_country_skip(message: Message, state: FSMContext):
    await state.update_data(country=valid_country(message.text))

    data = await state.get_data()

    random_data = []

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
            random_data.append(some_data)
        elif isinstance(some_data, str):
            await message.answer(
                text=some_data,
                reply_markup=main_kb(),
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


@router.message(RandomFilmSerial.country)
async def random_film_serial_country_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы\n"
             "написали страну(ы) которые хотите включить в рандомный поиск.\n"
    )