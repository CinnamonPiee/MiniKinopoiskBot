from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.history_of_search import HistoryOfSearch
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.back_kb import back_kb
from utils.date_valid import date_valid

router = Router(name=__name__)


@router.message(HistoryOfSearch.second_date, F.text == "Назад")
async def second_date_back(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.choose_film_serial_all)
    await message.answer(
        text="Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
        "или нажмите на кнопку <Пропустить> внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(HistoryOfSearch.second_date, F.text.cast(date_valid).as_("second_date"))
async def second_date(message: Message, state: FSMContext):
    await state.update_data(second_date=message.text)
    await ...
    await state.clear()


@router.message(HistoryOfSearch.second_date)
async def second_date_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Пожалуйста, введите конечную дату поиска (в формате ГГГГ-ММ-ДД)",
        reply_markup=back_kb(),
    )
