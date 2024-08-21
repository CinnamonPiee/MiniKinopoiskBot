from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_movie_length import valid_movie_length


router = Router(name=__name__)


@router.message(RandomFilmSerial.movie_length, F.text == "🚫 Назад 🚫")
async def random_film_serial_movie_length_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите возрастной рейтинг или промежуток\n"
             "за который хотите осуществить поиск, например\n"
             "(6, 12-18).\n"
             "Минимальный - 0\n"
             "Максимальный - 18",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_movie_length_skip(message: Message, state: FSMContext):
    await state.update_data(movie_length=None)
    await state.update_data(series_length=None)

    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите жанр(ы), если хотите несколько жанров,\n"
             "то напишите их через пробел, например\n"
             "(боевик, драма комедия).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length, F.text.cast(valid_movie_length).as_("movie_length"))
async def random_film_serial_movie_length_skip(message: Message, state: FSMContext):
    await state.update_data(movie_length=message.text)
    await state.update_data(series_length=None)

    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите жанр(ы), если хотите несколько жанров,\n"
             "то напишите их через пробел, например\n"
             "(боевик, драма комедия).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length)
async def random_film_serial_movie_length_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы\n"
             "написали продолжительность фильма который хотите\n"
             "включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )