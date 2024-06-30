from aiogram import Router, F
import json

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.find_film_serial import FindFilmSerial
from states.main_menu import MainMenu
from keyboards.reply.choose_criteries_kb import choose_criteries_kb
from api.movie_search import movie_search

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
    data = movie_search(str(F.text))
    await message.answer(text=f"Name: {data}")


@router.message(FindFilmSerial.name)
async def find_film_serial_name_none(message: Message):
    await message.answer(text="Sorry, I don`t understand. Please write correct film name!")
