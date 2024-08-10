from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations import valid_years


router = Router(name=__name__)


@router.message(CustomSearching.year, F.text == "Назад")
async def custom_searching_year_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.janr)
    await message.answer(
        text="Напишите пожалуйста жанр(ы), если хотите несколько жанров, то напишите их через пробел, например(боевик, драма комедия)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.year, F.text == "Пропустить")
async def custom_searching_year_skip(message: Message, state: FSMContext):
    await state.update_data(year=None)
    await state.set_state(CustomSearching.rating)
    await message.answer(
        text="Напишите пожалуйста рейтинг или отрывок за который хотите осуществить поиск, например (7, 7.1, 8-9.4)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.year, F.text.cast(valid_years.valid_years).as_("year"))
async def custom_searching_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(CustomSearching.rating)
    await message.answer(
        text="Напишите пожалуйста рейтинг или отрывок за который хотите осуществить поиск, например (7, 7.1, 8-9.4)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.year)
async def custom_searching_year_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали год который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
