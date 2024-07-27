from aiogram import Router, F
from states.random_film_serial import RandomFilmSerial
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.yes_no_back import yes_no_back
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)
PER_PAGE = 1


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Назад")
async def random_film_serial_criteries_yes_or_no_back(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.count)
    await message.answer(
        text="Укажите количество которое вы хотите получить: ",
        reply_markup=back_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Нет")
async def random_film_serial_criteries_yer_or_no(message: Message, state: FSMContext):
    TODO # Настроить вывод рандомных фильмов или сериалов без критериев. Необходимо 
    # сделать пагинацию на странице из рандомных фильмов или сериалов
    ...
    await state.clear()


@router.message(RandomFilmSerial.criteries_yes_or_no, F.text == "Да")
async def random_film_serial_criteries_yes_or_no(message: Message, state: FSMContext):
    await state.set_state(RandomFilmSerial.year)
    await message.answer(
        text="Напишите пожалуйста год или отрывок за который хотите осуществить поиск, например (2016, 2008-2010)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(RandomFilmSerial.criteries_yes_or_no)
async def random_film_serial_criteries_yes_or_no_none(message: Message):
    await message.answer(
        text="Я вас не понял, выберите пожалуйста хотите ли вы сделать рандомный поиск более подробным?",
        reply_markup=yes_no_back(),
    )
