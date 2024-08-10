from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.custom_searching import CustomSearching

from keyboards.reply.back_or_skip_kb import back_or_skip_kb

from utils.validations import valid_movie_length


router = Router(name=__name__)


@router.message(CustomSearching.movie_length, F.text == "Назад")
async def custom_searching_movie_length_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.country)
    await message.answer(
        text="Напишите пожалуйста страну(ы), если хотите несколько старн, то напишите их через пробел, например(США, Индия Канада)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.movie_length, F.text == "Пропустить")
async def custom_searching_movie_length_skip(message: Message, state: FSMContext):
    data = await state.update_data(movie_length=None)
    
    # TODO # Написать вывод на экран


@router.message(CustomSearching.movie_length, F.text.cast(valid_movie_length.valid_movie_length).as_("movie_length"))
async def custom_searching_movie_length(message: Message, state: FSMContext):
    data = await state.update_data(movie_length=message.text)

    # TODO  # Написать вывод на экран


@router.message(CustomSearching.movie_length)
async def custom_searching_movie_length_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали продолжительность фильма который хотите включить в рандомный поиск",
        reply_markup=back_or_skip_kb(),
    )
