from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.yes_no_back import yes_no_back
from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_years import valid_years


router = Router(name=__name__)


@router.message(RandomFilmSerial.year, F.text == "🚫 Назад 🚫")
async def random_film_serial_year_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.criteries_yes_or_no)
    await message.answer(
        text="Хотите настроить рандомный поиск более подробно?",
        reply_markup=yes_no_back(),
    )


@router.message(RandomFilmSerial.year, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_year_skip(message: Message, state: FSMContext):
    await state.update_data(year=None)
    await state.set_state(RandomFilmSerial.rating)
    await message.answer(
        text="Напишите рейтинг или отрывок за который\n"
             "хотите осуществить поиск, например (7, 7.1, 8-9.4).\n"
             "Минимальный - 1\n"
             "Максимальный - 10",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.year, F.text.cast(valid_years).as_("year"))
async def random_film_serial_year_skip(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(RandomFilmSerial.rating)
    await message.answer(
        text="Напишите рейтинг или отрывок за который\n"
             "хотите осуществить поиск, например (7, 7.1, 8-9.4).\n"
             "Минимальный - 1\n"
             "Максимальный - 10",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.year)
async def random_film_serial_year_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔.\n"
             "Необходимо что бы вы написали год\n"
             "который хотите включить в рандомный поиск.",
        reply_markup=back_or_skip_kb(),
    )
    