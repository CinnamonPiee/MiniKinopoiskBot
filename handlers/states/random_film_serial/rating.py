from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply.back_or_skip_kb import back_or_skip_kb


router = Router(name=__name__)


@router.message(RandomFilmSerial.rating, F.text == "Назад")
async def random_film_serial_rating_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.year)
    await message.answer(
        text="Напишите пожалуйста год или отрывок за который хотите осуществить поиск, например (2016, 2008-2010)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.rating, F.text == "Пропустить")
async def random_film_serial_rating_skip(message: Message, state: FSMContext):
    await state.update_data(rating=None)
    await state.set_state(RandomFilmSerial.age_rating)
    await message.answer(
        text="Напишите пожалуйста возрастной рейтинг или отрывок за который хотите осуществить поиск, например (2016, "
             "2008-2010)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.rating, F.)