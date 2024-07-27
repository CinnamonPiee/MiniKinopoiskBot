from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from utils.valid_age_rating import valid_age_rating


router = Router(name=__name__)


@router.message(RandomFilmSerial.age_rating, F.text == "Назад")
async def random_film_serial_age_rating_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.rating)
    await message.answer(
        text="Напишите пожалуйста рейтинг или отрывок за который хотите осуществить поиск, например (7, 7.1, 8-9.4)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.age_rating, F.text == "Пропустить")
async def random_film_serial_age_rating_skip(message: Message, state: FSMContext):
    data = state.get_data()
    if data["type_choice"] == "Сериалы":
        await state.set_state(RandomFilmSerial.series_length)
        await state.update_data(age_rating=None)
        await message.answer(
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "Фильмы":
        await state.set_state(RandomFilmSerial.movie_length)
        await state.update_data(age_rating=None)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "Фильмы и сериалы":
        await state.set_state(RandomFilmSerial.janr)
        await state.update_data(age_rating=None)
        await message.answer(
            text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.age_rating, F.text.cast(valid_age_rating).as_("age_rating"))
async def random_film_serial_age_rating(message: Message, state: FSMContext):
    data = state.get_data()
    if data["type_choice"] == "Сериалы":
        await state.set_state(RandomFilmSerial.series_length)
        await state.update_data(age_rating=message.text)
        await message.answer(
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "Фильмы":
        await state.set_state(RandomFilmSerial.movie_length)
        await state.update_data(age_rating=message.text)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "Фильмы и сериалы":
        await state.set_state(RandomFilmSerial.janr)
        await state.update_data(age_rating=message.text)
        await message.answer(
            text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.age_rating)
async def random_film_serial_age_rating_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали возрастной рейтинг который хотите включить в рандомный поиск"
    )
