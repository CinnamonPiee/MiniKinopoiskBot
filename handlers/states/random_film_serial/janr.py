from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply.back_or_skip_kb import back_or_skip_kb


router = Router(name=__name__)


@router.message(RandomFilmSerial.janr, F.text == "Назад")
async def random_film_serial_janr_back(message: Message, state: FSMContext):
    data = state.get_data()
    if data["type_choice"] == "Фильмы":
        await state.set_state(RandomFilmSerial.movie_length)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Сериалы":
        await state.set_state(RandomFilmSerial.series_length)
        await message.answer(
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Фильмы и сериалы":
        await state.set_state(RandomFilmSerial.age_rating)
        await message.answer(
            text="Напишите пожалуйста возрастной рейтинг или промежуток за который хотите осуществить поиск, например (6, "
            "12-18)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )


@router.message(RandomFilmSerial.janr, F.text == "Пропустить")
async def random_film_serial_janr_skip(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.country)
    await state.update_data(janr=None)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться."
        reply_markup=back_or_skip_kb(),
    )

TODO # Написать проверку на правильный ввод стран
@router.message(RandomFilmSerial.janr, F.text.cast().as_("janr"))
async def random_film_serial_janr(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.country)
    await state.update_data(janr=message.text)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.janr)
async def random_film_serial_janr_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали жанр(ы) которые хотите включить в рандомный поиск."
    )