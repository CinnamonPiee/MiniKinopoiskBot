from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from aiogram.utils import markdown
from keyboards.reply.back_kb import back_kb
from keyboards.reply.yes_no_back import yes_no_back
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from database.orm.film import add_film, film_exists
from database.orm.serial import add_serial, serial_exists
from keyboards.inline.create_random_pagination_kb import create_random_pagination_kb
from aiogram.fsm.context import FSMContext
from api.random_history_movie_serial_search import random_history_movie_serial_search
from utils.validations import Validations
from aiogram.types import FSInputFile


router = Router(name=__name__)
PER_PAGE = 1


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Назад")
async def random_film_serial_criteries_yes_or_no_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.count)
    await message.answer(
        text="Укажите количество которое вы хотите получить: ",
        reply_markup=back_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Нет")
async def random_film_serial_criteries_yer_or_no(message: Message, state: FSMContext):
    data = await state.get_data()
    random_data = []
    for _ in range(int(data["count"])):
        some_data = random_history_movie_serial_search(type_choice=data["type_choice"])
        if isinstance(some_data, dict):
            random_data.append(some_data)
        elif isinstance(some_data, str):
            await message.answer(
                text="Сервис временно не доступен, попробуйте позже!"
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
        if item["poster"]["previewUrl"] is not None and Validations.get_valid_url(item["poster"]["previewUrl"]):
            url = item["poster"]["previewUrl"]
        else:
            url = FSInputFile("/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg")
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
            await Validations.valid_user_and_film_id_in_history(name, telegram_id=message.from_user.id)

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

        caption=f"{markdown.hbold(name)}\n"\
                f"Жанры: {genres}\n"\
                f"Рейтинг: {rating}\n"\
                f"Год: {year}\n"\
                f"Продолжительность фильма: {movie_length}\n"\
                f"Страна: {countries}\n"\
                f"Возрастной рейтинг: {age_rating}\n"\
                f"Описание: {description}"\

        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=url,
            caption=caption,
            reply_markup=keyboards,
        )

    elif item["type"] == "tv-series":
        if item["poster"]["previewUrl"] is not None and Validations.get_valid_url(item["poster"]["previewUrl"]):
            url = item["poster"]["previewUrl"]
        else:
            url = FSInputFile(
                "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg")
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
            await Validations.valid_user_and_serial_id_in_history(name, telegram_id=message.from_user.id)

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
                
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=url,
            caption=caption,
            reply_markup=keyboards,
        )


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Да")
async def random_film_serial_criteries_yes_or_no(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.year)
    await message.answer(
        text="Напишите пожалуйста год или отрывок за который хотите осуществить поиск, например (2016, 2008-2010)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no)
async def random_film_serial_criteries_yes_or_no_none(message: Message):
    await message.answer(
        text="Я вас не понял, выберите пожалуйста хотите ли вы сделать рандомный поиск более подробным?",
        reply_markup=yes_no_back(),
    )
