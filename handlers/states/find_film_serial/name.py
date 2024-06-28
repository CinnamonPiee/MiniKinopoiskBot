from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.find_film_serial import FindFilmSerial
from states.main_menu import MainMenu
from keyboards.reply.choose_criteries_kb import choose_criteries_kb

router = Router(name=__name__)


@router.message(FindFilmSerial.name, F.text == "Back")
async def find_film_serial_name_none(message: Message, state: FSMContext):
    await state.set_state(MainMenu.criteries)
    await message.answer(
        text="Choose please what you want to find: ",
        reply_markup=choose_criteries_kb(),
    )


@router.message(FindFilmSerial.name, F.text)
async def find_film_serial_name(message: Message, state: FSMContext):
    if True:
        pass  # Если данный фильм найден, то вывести его пользователю
        # Если данного фильма не нашлось, то попросить ввести корректное название или попробовать
        # ввести другое название фильма


@router.message(FindFilmSerial.name)
async def find_film_serial_name_none(message: Message):
    await message.answer(text="Please write correct film name!")
