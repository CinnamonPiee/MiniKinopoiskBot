from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from states import (
    main_menu,
    find_film_serial,
    random_film_serial,
    low_coast_film_or_serial,
    height_coast_film_or_serial,
    custom_searching
)

from keyboards.reply import (
    main_kb,
    choose_criteries_kb,
    back_kb,
    choose_random_film_serial_kb
)


router = Router(name=__name__)


@router.message(F.text == "Фильмы / Сериалы", default_state)
async def main_choose_start(message: Message, state: FSMContext):
    await state.set_state(main_menu.MainMenu.criteries)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=choose_criteries_kb.choose_criteries_kb(),
    )


@router.message(main_menu.MainMenu.criteries, F.text == "Найти фильм / сериал")
async def main_choose_find_film_serial(message: Message, state: FSMContext):
    await state.set_state(find_film_serial.FindFilmSerial.name)
    await message.answer(
        text="Пожалуйста, введите название фильма или сериала: ",
        reply_markup=back_kb.back_kb(),
        parse_mode=None,
        )


@router.message(main_menu.MainMenu.criteries, F.text == "Рандомный фильм/ сериал")
async def main_choose_random_film_serial(message: Message, state: FSMContext):
    await state.set_state(random_film_serial.RandomFilmSerial.type)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите получить рандомно: ",
        reply_markup=choose_random_film_serial_kb.choose_random_film_serial_kb(),
        parse_mode=None,
    )


@router.message(main_menu.MainMenu.criteries, F.text == "Малобюджетный фильм / сериал")
async def main_choose_low_coast_film_serial(message: Message, state: FSMContext):
    await state.set_state(low_coast_film_or_serial.LowCoastFilmSerial.criteries_yes_or_no)


@router.message(main_menu.MainMenu.criteries, F.text == "Высоко бюджетный фильм / сериал")
async def main_choose_height_coast_film_serial(message: Message, state: FSMContext):
    await state.set_state(height_coast_film_or_serial.HeightCoastFilmSerial.criteries_yes_or_no)


@router.message(main_menu.MainMenu.criteries, F.text == "Кастомный поиск")
async def main_choose_custom_searching(message: Message, state: FSMContext):
    await state.set_state(custom_searching.CustomSearching.janr)


@router.message(main_menu.MainMenu.criteries, F.text == "Назад")
async def main_choose_back(message: Message, state: FSMContext):
    await message.answer(
        text="Может быть в другой раз...",
        reply_markup=main_kb.main_kb(),
    )
    await state.clear()


@router.message(main_menu.MainMenu.criteries)
async def main_choose_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю. Выберите пожалуйста что вы хотите найти!",
        reply_markup=choose_criteries_kb.choose_criteries_kb())
