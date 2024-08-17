from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations.valid_rating import valid_rating


router = Router(name=__name__)


@router.message(RandomFilmSerial.rating, F.text == "🚫 Назад 🚫")
async def random_film_serial_rating_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.year)
    await message.answer(
        text="Напишите год или отрывок за который"
             "хотите осуществить поиск, например (2016, 2008-2010).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.rating, F.text == "⏩ Пропустить ⏩")
async def random_film_serial_rating_skip(message: Message, state: FSMContext):
    await state.update_data(rating=None)

    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите возрастной рейтинг или промежуток"
             "за который хотите осуществить поиск, например"
             "(6, 12-18).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.rating, F.text.cast(valid_rating).as_("rating"))
async def random_film_serial_rating_skip(message: Message, state: FSMContext):
    await state.update_data(rating=message.text)

    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите возрастной рейтинг или промежуток"
             "за который хотите осуществить поиск, например"
             "(6, 12-18).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.rating)
async def random_film_serial_rating_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы"
             "написали рейтинг который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )