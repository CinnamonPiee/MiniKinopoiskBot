from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.history_search_kb import history_search_kb

from utils.validations.valid_num import valid_num

from states.custom_searching import CustomSearching


router = Router(name=__name__)


@router.message(CustomSearching.count, F.text == "🚫 Назад 🚫")
async def custom_searching_count_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.type_choice)
    await message.answer(
        text="Выберите что вы хотите получить рандомно. ",
        reply_markup=history_search_kb(),
    )


@router.message(CustomSearching.count, F.text.cast(valid_num).as_("count"))
async def custom_searching_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    await state.set_state(CustomSearching.janr)
    await message.answer(
        text="Напишите жанр(ы), если хотите несколько жанров, то"
             "напишите их через пробел, например(боевик, драма комедия).",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.count)
async def custom_searching_count_none(message: Message):
    await message.answer(
        text="Я вас не понял 😔. Необходимо написать"
             "количество которое вы хотите видеть!",
        reply_markup=back_kb(),
    )
