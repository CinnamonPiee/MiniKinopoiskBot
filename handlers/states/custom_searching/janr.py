from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.back_kb import back_kb

from utils.validations.valid_janr import valid_janr

from states.custom_searching import CustomSearching


router = Router(name=__name__)


@router.message(CustomSearching.janr, F.text == "🚫 Назад 🚫")
async def custom_searching_janr_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.count)
    await message.answer(
        text="Укажите количество которое хотите получить.",
        reply_markup=back_kb(),
    )


@router.message(CustomSearching.janr, F.text == "⏩ Пропустить ⏩")
async def custom_searching_janr_skip(message: Message, state: FSMContext):
    await state.update_data(janr=None)
    
    await state.set_state(CustomSearching.year)
    await message.answer(
        text="Напишите год или отрывок за который\n"
             "хотите осуществить поиск, например\n"
             "(2016, 2008-2010).\n"
             "Максимальный - 2024",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.janr, F.text.cast(valid_janr).as_("janr"))
async def custom_searching_janr_skip(message: Message, state: FSMContext):
    await state.update_data(janr=message.text)

    await state.set_state(CustomSearching.year)
    await message.answer(
        text="Напишите год или отрывок за который"
             "хотите осуществить поиск, например\n"
             "(2016, 2008-2010).\n"
             "Максимальный - 2024",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.janr)
async def custom_searching_janr_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо что бы вы написали\n"
             "жанр(ы) которые хотите включить в рандомный поиск."
    )
