from aiogram import Router, F

from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_custom_pagination_kb import create_custom_pagination_kb

from utils.validations.valid_movie_length import valid_movie_length
from utils.validations.valid_url import valid_url
from utils.validations.valid_user_and_film_id_in_history import valid_user_and_film_id_in_history

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from database.orm.film import add_film, film_exists


router = Router(name=__name__)


@router.message(CustomSearching.movie_length, F.text == "Назад")
async def custom_searching_movie_length_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.country)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.movie_length, F.text == "Пропустить")
async def custom_searching_movie_length_skip(message: Message, state: FSMContext):
    await state.update_data(movie_length=None)
    data = await state.get_data()

    if data["type_choice"] == "movie":
        await state.update_data(series_length=None)
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
                    text="Сервис временно не доступен, попробуйте позже!"
                )
                await state.clear()
                break

        if random_data:
            await state.update_data(
                random_data=random_data, 
                page=0, 
                telegram_id=message.from_user.id
            )

        item = random_data[0]
        page = 0
        total_count = len(random_data)
        keyboards = create_custom_pagination_kb(page, total_count)

        # TODO доделать присвоение через функцию
        url, name, genres


        if item["poster"]["previewUrl"] is not None and valid_url(item["poster"]["previewUrl"]):
            url = item["poster"]["previewUrl"]
        else:
            url = FSInputFile(
                "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
            )
        if item["name"] == None:
            name = ""
        else:
            name = item["name"]
        if item["genres"] == None:
            genres = ""
        else:
            genres = ', '.join([i["name"] for i in item["genres"]])
        if item["rating"]["imdb"] == None:
            rating = ""
        else:
            rating = item["rating"]["imdb"]
        if item["year"] == None:
            year = 0
        else:
            year = item["year"]
        if item["movieLength"] == None:
            movie_length = 0
        else:
            movie_length = str(int(item["movieLength"]) // 60) + ":" + str(
                int(item["movieLength"]) % 60)
        if item["countries"] == None:
            countries = ""
        else:
            countries = ', '.join([i["name"] for i in item["countries"]])
        if item["ageRating"] == None:
            age_rating = 0
        else:
            age_rating = item["ageRating"]
        if item["shortDescription"] == None or item["shortDescription"] == "":
            if item["description"] == None:
                description = ""
            else:
                description = item["description"]
        else:
            description = item["shortDescription"]

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
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(CustomSearching.movie_length, F.text.cast(valid_movie_length).as_("movie_length"))
async def custom_searching_movie_length(message: Message, state: FSMContext):
    await state.update_data(movie_length=message.text)
    data = await state.get_data()

    if data["type_choice"] == "movie":
        await state.update_data(series_length=None)
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
                    text="Сервис временно не доступен, попробуйте позже!"
                )
                await state.clear()
                break

        if random_data:
            await state.update_data(
                random_data=random_data, 
                page=0, 
                telegram_id=message.from_user.id
            )

        item = random_data[0]
        page = 0
        total_count = len(random_data)
        keyboards = create_custom_pagination_kb(page, total_count)


        if item["poster"]["previewUrl"] is not None and valid_url(item["poster"]["previewUrl"]):
            url = item["poster"]["previewUrl"]
        else:
            url = FSInputFile(
                "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
            )
        if item["name"] == None:
            name = ""
        else:
            name = item["name"]
        if item["genres"] == None:
            genres = ""
        else:
            genres = ', '.join([i["name"] for i in item["genres"]])
        if item["rating"]["imdb"] == None:
            rating = ""
        else:
            rating = item["rating"]["imdb"]
        if item["year"] == None:
            year = 0
        else:
            year = item["year"]
        if item["movieLength"] == None:
            movie_length = 0
        else:
            movie_length = str(int(item["movieLength"]) // 60) + ":" + str(
                int(item["movieLength"]) % 60)
        if item["countries"] == None:
            countries = ""
        else:
            countries = ', '.join([i["name"] for i in item["countries"]])
        if item["ageRating"] == None:
            age_rating = 0
        else:
            age_rating = item["ageRating"]
        if item["shortDescription"] == None or item["shortDescription"] == "":
            if item["description"] == None:
                description = ""
            else:
                description = item["description"]
        else:
            description = item["shortDescription"]

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
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(CustomSearching.movie_length)
async def custom_searching_movie_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность фильма который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
