from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_series_length import valid_series_length


router = Router(name=__name__)


@router.message(RandomFilmSerial.series_length, F.text == "Назад")
async def random_film_serial_series_length_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите пожалуйста возрастной рейтинг или промежуток за который хотите осуществить поиск, например (6, "
             "12-18)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.series_length, 
    F.text == "Пропустить" or F.text.cast(valid_series_length).as_("series_length"))
async def random_film_serial_series_length_skip(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        await state.update_data(series_length=None)
        await state.update_data(movie_length=None)
    else:
        await state.update_data(series_length=message.text)
        await state.update_data(movie_length=None)

    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.series_length)
async def random_film_serial_series_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность серии которую хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )