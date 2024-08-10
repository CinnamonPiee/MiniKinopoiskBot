from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations import valid_movie_length


router = Router(name=__name__)


@router.message(RandomFilmSerial.movie_length, F.text == "Назад")
async def random_film_serial_movie_length_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите пожалуйста возрастной рейтинг или промежуток за который хотите осуществить поиск, например (6, "
             "12-18)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length, F.text == "Пропустить")
async def random_film_serial_movie_length_skip(message: Message, state: FSMContext):
    await state.update_data(movie_length=None)
    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length, F.text.cast(valid_movie_length.valid_movie_length).as_("movie_length"))
async def random_film_serial_movie_length(message: Message, state: FSMContext):
    await state.update_data(series_length=None)
    await state.update_data(movie_length=message.text)
    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.movie_length)
async def random_film_serial_movie_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность фильма который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )