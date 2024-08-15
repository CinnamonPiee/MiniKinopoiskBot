from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.random_film_serial import RandomFilmSerial
from states.main_menu import MainMenu

from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.back_kb import back_kb
from keyboards.reply.choose_criteries_kb import choose_criteries_kb

from utils.validations.valid_choose_in_type import valid_choose_in_type


router = Router(name=__name__)


@router.message(RandomFilmSerial.type_choice, F.text == "Назад")
async def random_film_serial_type_choice_back(message: Message, state: FSMContext):
    await state.set_state(MainMenu.criteries)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=choose_criteries_kb(),
    )


@router.message(RandomFilmSerial.type_choice, 
    F.text.cast(valid_choose_in_type).as_("type_choice"))
async def random_film_serial_type_choice(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.count)
    if message.text == "Фильмы":
        await state.update_data(type_choice="movie")
        await message.answer(
            text="Укажите количество которое хотите получить: ",
            reply_markup=back_kb(),
        )
    elif message.text == "Сериалы":
        await state.update_data(type_choice="tv-series")
        await message.answer(
            text="Укажите количество которое хотите получить: ",
            reply_markup=back_kb(),
        )
    elif message.text == "Фильмы и сериалы":
        await state.update_data(type_choice=None)
        await message.answer(
            text="Укажите количество которое хотите получить: ",
            reply_markup=back_kb(),
        )
    


@router.message(RandomFilmSerial.type_choice)
async def random_film_serial_type_choice_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю, выберите пожалуйста что вы хотите найти, фильм, сериал или все вместе!",
        reply_markup=history_search_kb(),
    )
