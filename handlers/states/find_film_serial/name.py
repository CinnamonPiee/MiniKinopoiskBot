from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.find_film_serial import FindFilmSerial
from states.main_menu import MainMenu

from keyboards.reply.choose_criteries_kb import choose_criteries_kb
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_kb import back_kb

from database.orm.film import add_film, film_exists
from database.orm.serial import add_serial, serial_exists

from utils.get_film_data import get_film_data
from utils.get_serial_data import get_serial_data
from utils.validations.valid_user_and_film_id_in_history import valid_user_and_film_id_in_history
from utils.validations.valid_user_and_serial_id_in_history import valid_user_and_serial_id_in_history

from api.movie_serial_search import movie_serial_search


router = Router(name=__name__)


@router.message(FindFilmSerial.name, F.text == "🚫 Назад 🚫")
async def find_film_serial_name_none(message: Message, state: FSMContext):
    await state.set_state(MainMenu.criteries)
    await message.answer(
        text="Выберите что вы хотите найти. ⬇️",
        reply_markup=choose_criteries_kb(),
    )


@router.message(FindFilmSerial.name, F.text)
async def find_film_serial_name(message: Message, state: FSMContext):
    data = movie_serial_search(message.text)
    if isinstance(data, str):
        await message.answer(
            text=data,
            reply_markup=back_kb(),
            parse_mode=None,
        )

    elif isinstance(data, dict):
        if data["type"] == "movie":
            (url,
             name,
             genres,
             rating,
             year,
             movie_length,
             countries,
             age_rating,
             description) = get_film_data(data)

            try:
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=url,
                    caption=f"{markdown.hbold(name)}\n"
                            f"Жанры: {genres}\n"
                            f"Рейтинг: {rating}\n"
                            f"Год: {year}\n"
                            f"Продолжительность фильма: {movie_length}\n"
                            f"Страна: {countries}\n"
                            f"Возрастной рейтинг: {age_rating}\n"
                            f"Описание: {description}",
                    reply_markup=main_kb(),
                )
                
            except:
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=url,
                    caption=f"{markdown.hbold(name)}\n"
                    f"Жанры: {genres}\n"
                    f"Рейтинг: {rating}\n"
                    f"Год: {year}\n"
                    f"Продолжительность фильма: {movie_length}\n"
                    f"Страна: {countries}\n"
                    f"Возрастной рейтинг: {age_rating}\n"
                    f"Описание: None",
                    reply_markup=main_kb(),
                )

            if await film_exists(name):
                await valid_user_and_film_id_in_history(name, telegram_id=message.from_user.id)

            else:
                if data["movieLength"] == None:
                    movie_length = 0
                else:
                    movie_length = int(data["movieLength"])
                await add_film(
                    telegram_id=message.from_user.id,
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

                await state.clear()

        elif data["type"] == "tv-series":
            (url,
             name,
             genres,
             rating,
             release_years,
             series_length,
             countries,
             age_rating,
             description) = get_serial_data(data)

            try:
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=url,
                    caption=f"{markdown.hbold(name)}\n"
                            f"Жанры: {genres}\n"
                            f"Рейтинг: {rating}\n"
                            f"Релиз: {release_years}\n"
                            f"Продолжительность серии: {series_length}\n"
                            f"Страна: {countries}\n"
                            f"Возрастной рейтинг: {age_rating}\n"
                            f"Описание: {description}",
                    reply_markup=main_kb(),
                )

            except:
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=url,
                    caption=f"{markdown.hbold(name)}\n"
                            f"Жанры: {genres}\n"
                            f"Рейтинг: {rating}\n"
                            f"Релиз: {release_years}\n"
                            f"Продолжительность серии: {series_length}\n"
                            f"Страна: {countries}\n"
                            f"Возрастной рейтинг: {age_rating}\n"
                            f"Описание: None",
                    reply_markup=main_kb(),
                )

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

                await state.clear()


@router.message(FindFilmSerial.name)
async def find_film_serial_name_none(message: Message):
    await message.answer(
        text="Я не понимаю 😔. Напишите корректное название фильма!",
        reply_markup=back_kb(),
    )
