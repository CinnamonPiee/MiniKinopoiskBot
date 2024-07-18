from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from keyboards.reply.choose_criteries_kb import choose_criteries_kb
from states.main_menu import MainMenu
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)


@router.message(RandomFilmSerial.type, F.text == "Назад")
async def random_film_serial_type_none(message: Message, state: FSMContext):
    await state.set_state(MainMenu.criteries)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=choose_criteries_kb(),
    )


@router.message(RandomFilmSerial.type, F.text)
async def random_film_serial_type(message: Message, state: FSMContext):



