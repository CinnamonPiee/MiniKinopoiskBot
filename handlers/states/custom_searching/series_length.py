from aiogram import Router, F

from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.inline.create_custom_pagination_kb import create_custom_pagination_kb

from utils.validations import (
    valid_url,
    valid_user_and_serial_id_in_history,
    valid_series_length
)

from api.random_custom_movie_serial_search import random_custom_movie_serial_search

from database.orm.serial import add_serial, serial_exists


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


@router.message(CustomSearching.series_length, F.text == "Пропустить")
async def custom_searching_series_length_skip(message: Message, state: FSMContext):
    await state.update_data(series_length=None)

    data = state.get_data()

    if data["type_choice"] == "tv-series":
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

        if item["poster"]["previewUrl"] is not None and valid_url.valid_url(item["poster"]["previewUrl"]):
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
        if item["releaseYears"] == None:
            release_years = ""
        else:
            release_years = str(
                item["releaseYears"][0]["start"]) + " - " + str(item["releaseYears"][0]["end"])
        if item["seriesLength"] == None:
            series_length = ""
        else:
            series_length = str(item["seriesLength"]) + " минут"
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

        if await serial_exists(name):
            await valid_user_and_serial_id_in_history.valid_user_and_serial_id_in_history(
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

    elif data["type_choice"] == None:
        # TODO # Написать вывод на экран


@router.message(CustomSearching.series_length, F.text.cast(valid_series_length.valid_series_length).as_("series_length"))
async def custom_searching_series_length(message: Message, state: FSMContext):
    await state.update_data(series_length=message.text)
    data = state.get_data()

    # TODO  # Написать вывод на экран


@router.message(CustomSearching.series_length)
async def custom_searching_series_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность серии которую хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
