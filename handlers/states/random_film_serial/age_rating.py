from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_age_rating import valid_age_rating

router = Router(name=__name__)


@router.message(RandomFilmSerial.age_rating, F.text == "🚫 Назад 🚫")
async def random_film_serial_age_rating_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.rating)
    await message.answer(
        text="Напишите рейтинг или отрывок за который"
             "хотите осуществить поиск, например (7, 7.1, 8-9.4).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.age_rating, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_age_rating_skip(message: Message, state: FSMContext):
    await state.update_data(age_rating=None)

    data = await state.get_data()
    if data["type_choice"] == "tv-series":
        await state.set_state(RandomFilmSerial.series_length)
        await message.answer(
            text="Напишите продолжительность серии или отрывок"
                 "за который хотите осуществить поиск, например (40, 30-60).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "movie":
        await state.set_state(RandomFilmSerial.movie_length)
        await message.answer(
            text="Напишите продолжительность фильма или отрывок"
                 "за который хотите осуществить поиск, например (120, 100-160).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == None:
        await state.set_state(RandomFilmSerial.janr)
        await message.answer(
            text="Напишите жанр(ы), если хотите несколько жанров,"
                 "то напишите их через пробел, например(боевик, драма комедия).",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.age_rating, F.text.cast(valid_age_rating).as_("age_rating"))
async def random_film_serial_age_rating_skip(message: Message, state: FSMContext):
    await state.update_data(age_rating=message.text)

    data = await state.get_data()
    if data["type_choice"] == "tv-series":
        await state.set_state(RandomFilmSerial.series_length)
        await message.answer(
            text="Напишите продолжительность серии или отрывок"
                 "за который хотите осуществить поиск, например (40, 30-60).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "movie":
        await state.set_state(RandomFilmSerial.movie_length)
        await message.answer(
            text="Напишите продолжительность фильма или отрывок"
                 "за который хотите осуществить поиск, например (120, 100-160).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == None:
        await state.set_state(RandomFilmSerial.janr)
        await message.answer(
            text="Напишите жанр(ы), если хотите несколько жанров,"
                 "то напишите их через пробел, например(боевик, драма комедия).",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.age_rating)
async def random_film_serial_age_rating_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы написали"
             "возрастной рейтинг который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
