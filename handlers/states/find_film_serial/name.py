from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from states.find_film_serial import FindFilmSerial
from states.main_menu import MainMenu
from keyboards.reply.choose_criteries_kb import choose_criteries_kb
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_kb import back_kb
from api.movie_search import movie_search

router = Router(name=__name__)


@router.message(FindFilmSerial.name, F.text == "Назад")
async def find_film_serial_name_none(message: Message, state: FSMContext):
    await state.set_state(MainMenu.criteries)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=choose_criteries_kb(),
    )


@router.message(FindFilmSerial.name, F.text)
async def find_film_serial_name(message: Message, state: FSMContext):
    data = movie_search(message.text)
    if isinstance(data, str):
        await message.answer(
            text=data,
            reply_markup=back_kb(),
            parse_mode=None,
        )

    elif isinstance(data, dict):
        if data["type"] == "movie":
            url = data["poster"]["previewUrl"]
            name = data["name"]
            genres = ', '.join([i["name"] for i in data["genres"]])
            rating = data["rating"]["imdb"]
            year = data["year"]
            movie_length = str(int(data["movieLength"]) // 60) + ":" + str(
                int(data["movieLength"]) % 60)
            countries = ', '.join([i["name"] for i in data["countries"]])
            age_rating = data["ageRating"]
            description = data["description"]

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
                reply_markup=main_kb())
            await state.clear()

        elif data["type"] == "tv-series":
            url = data["poster"]["previewUrl"]
            name = data["name"]
            genres = ', '.join([i["name"] for i in data["genres"]])
            rating = data["rating"]["imdb"]
            release_years = str(data["releaseYears"][0]["start"]) + " - " + str(data["releaseYears"][0]["end"])
            series_length = str(data["seriesLength"]) + " минут"
            countries = ', '.join([i["name"] for i in data["countries"]])
            age_rating = data["ageRating"]
            description = data["description"]

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
                reply_markup=main_kb())
            await state.clear()


@router.message(FindFilmSerial.name)
async def find_film_serial_name_none(message: Message):
    await message.answer(text="Простите, я не понимаю. Напишите пожалуйста корректное название фильма!")
