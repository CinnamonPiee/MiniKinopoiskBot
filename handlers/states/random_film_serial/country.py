from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from utils.validations import Validations

router = Router(name=__name__)


@router.message(RandomFilmSerial.country, F.text == "Назад")
async def random_film_serial_country_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.janr)
    await message.answer(
        text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.country, F.text == "Пропустить")
async def random_film_serial_country_skip(message: Message, state: FSMContext):
    data = await state.update_data(country=None)
    # TODO # Добавить вывод пользователю

    await state.clear()

@router.message(RandomFilmSerial.country, F.text.cast(Validations.valid_country).as_("country"))
async def random_film_serial_country(message: Message, state: FSMContext):
    data = await state.update_data(country=message.text)
    # TODO  # Добавить вывод пользователю

    await state.clear()


@router.message(RandomFilmSerial.country)
async def random_film_serial_country_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали страну(ы) которые хотите включить в рандомный поиск."
    )