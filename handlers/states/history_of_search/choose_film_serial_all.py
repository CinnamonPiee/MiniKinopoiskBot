from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.history_of_search import HistoryOfSearch

from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations import valid_choose_in_type


router = Router(name=__name__)


@router.message(F.text == "История поиска")
async def choose_film_serial_all_start(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.choose_film_serial_all)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=history_search_kb(),
    )


@router.message(HistoryOfSearch.choose_film_serial_all, F.text == "Назад")
async def choose_film_serial_all_start_back(message: Message, state: FSMContext):
    await message.answer(
        text="Может быть в другой раз...",
        reply_markup=main_kb(),
    )

    await state.clear()


@router.message(HistoryOfSearch.choose_film_serial_all, F.text.cast(valid_choose_in_type.valid_choose_in_type).as_("choice"))
async def process_choose_film_serial_all(message: Message, state: FSMContext):
    if message.text == "Фильмы":
        await state.update_data(choice="movie")
    elif message.text == "Сериалы":
        await state.update_data(choice="tv-series")
    elif message.text == "Фильмы и сериалы":
        await state.update_data(choice=None)
        
    await state.set_state(HistoryOfSearch.first_date)
    await message.answer(
        text="Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
        "или нажмите на кнопку 'Пропустить' внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb(),
        parse_mode=None,
    )


@router.message(HistoryOfSearch.choose_film_serial_all)
async def process_choose_film_serial_all_none(message: Message):
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=history_search_kb(),
    )
