from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations import valid_age_rating


router = Router(name=__name__)


@router.message(CustomSearching.age_rating, F.text == "Назад")
async def custom_searching_age_rating_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.rating)
    await message.answer(
        text="Напишите пожалуйста рейтинг или отрывок за который хотите осуществить поиск, например (7, 7.1, 8-9.4)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.age_rating, F.text == "Пропустить")
async def custom_searching_age_rating_skip(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.country)
    await state.update_data(age_rating=None)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.age_rating, F.text.cast(valid_age_rating.valid_age_rating).as_("age_rating"))
async def custom_searching_age_rating(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.country)
    await state.update_data(age_rating=message.text)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.age_rating)
async def custom_searching_age_rating_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали возрастной рейтинг который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
