from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.yes_no_back import yes_no_back
from aiogram.fsm.context import FSMContext
from utils.valid_num import valid_num


router = Router(name=__name__)


@router.message(RandomFilmSerial.count, F.text == "Назад")
async def random_film_serial_count_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.type_choice)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите получить рандомно: ",
        reply_markup=history_search_kb(),
    )


@router.message(RandomFilmSerial.count, F.text.cast(valid_num).as_("count"))
async def random_film_serial_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    await state.set_state(RandomFilmSerial.criteries_yes_or_no)
    await message.answer(
        text="Хотите ли вы настроить рандомный поиск более подробно?",
        reply_markup=yes_no_back(),
    )


@router.message(RandomFilmSerial.count)
async def random_film_serial_count_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо написать количество которое вы хотите видеть!"
    )
