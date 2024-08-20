from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_janr import valid_janr


router = Router(name=__name__)


@router.message(RandomFilmSerial.janr, F.text == "🚫 Назад 🚫")
async def random_film_serial_janr_back(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["type_choice"] == "movie":
        await state.set_state(RandomFilmSerial.movie_length)
        await message.answer(
            text="Напишите продолжительность фильма или отрывок"
                 "за который хотите осуществить поиск, например (120, 100-160).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == "tv-series":
        await state.set_state(RandomFilmSerial.series_length)
        await message.answer(
            text="Напишите продолжительность серии или отрывок"
                 "за который хотите осуществить поиск, например (40, 30-60).",
            reply_markup=back_or_skip_kb(),
        )

    elif data["type_choice"] == None:
        await state.set_state(RandomFilmSerial.age_rating)
        await message.answer(
            text="Напишите возрастной рейтинг или промежуток"
                 "за который хотите осуществить поиск, например"
                 "(6, 12-18).",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.janr, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_janr_skip(message: Message, state: FSMContext):
    await state.update_data(janr=None)
    
    await state.set_state(RandomFilmSerial.country)
    await message.answer(
        text="Напишите страну(ы), если хотите несколько стран,"
             "то напишите их через пробел, например(США, Индия Канада).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.janr, F.text.cast(valid_janr).as_("janr"))
async def random_film_serial_janr_skip(message: Message, state: FSMContext):
    await state.update_data(janr=message.text.split(" "))

    await state.set_state(RandomFilmSerial.country)
    await message.answer(
        text="Напишите страну(ы), если хотите несколько стран,"
             "то напишите их через пробел, например(США, Индия Канада).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.janr)
async def random_film_serial_janr_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы"
             "написали жанр(ы) которые хотите включить в рандомный поиск."
    )