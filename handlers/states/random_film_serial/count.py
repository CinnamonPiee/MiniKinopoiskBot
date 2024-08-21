from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial

from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.yes_no_back import yes_no_back

from utils.validations.valid_num import valid_num

from keyboards.reply.back_kb import back_kb


router = Router(name=__name__)


@router.message(RandomFilmSerial.count, F.text == "🚫 Назад 🚫")
async def random_film_serial_count_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.type_choice)
    await message.answer(
        text="Выберите что вы хотите получить рандомно.",
        reply_markup=history_search_kb(),
    )


@router.message(RandomFilmSerial.count, F.text.cast(valid_num).as_("count"))
async def random_film_serial_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    await state.set_state(RandomFilmSerial.criteries_yes_or_no)
    await message.answer(
        text="Хотите настроить рандомный поиск более подробно?",
        reply_markup=yes_no_back(),
    )


@router.message(RandomFilmSerial.count)
async def random_film_serial_count_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо написать\n"
             "количество которое вы хотите видеть!",
        reply_markup=back_kb(),
    )
