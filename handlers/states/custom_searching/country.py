from aiogram import Router, F
from states.custom_searching import CustomSearching
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply.back_or_skip_kb import back_or_skip_kb


router = Router(name=__name__)


@router.message(CustomSearching.country, F.text == "Назад")
async def custom_searching_country_back(message: Message, state: FSMContext):
    await state.set_state(CustomSearching.age_rating)
    await message.answer(
        text="Напишите пожалуйста возрастной рейтинг или промежуток за который хотите осуществить поиск, например (6, "
             "12-18)."
             "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
             "учитываться.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(CustomSearching.country, F.text == "Пропустить")
async def custom_searching_country_skip(message: Message, state: FSMContext):
    data = state.get_data()
    if data["type_choice"] == "Фильмы":
        await state.set_state(CustomSearching.movie_length)
        await state.update_data(country=None)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Сериалы":
        await state.set_state(CustomSearching.series_length)
        await state.update_data(country=None)
        await message.answer(
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Фильмы и сериалы":
        data = await state.update_data(country=None)
        # TODO # Доделать вывод на экран
    

# TODO  # Написать проверку на правильный ввод стран
@router.message(CustomSearching.country, F.text.cast(...).as_("country"))
async def custom_searching_country(message: Message, state: FSMContext):
    data = state.get_data()
    if data["type_choice"] == "Фильмы":
        await state.set_state(CustomSearching.movie_length)
        await state.update_data(country=message.text)
        await message.answer(
            text="Напишите пожалуйста продолжительность фильма или отрывок за который хотите осуществить поиск, например (120, 100-160)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Сериалы":
        await state.set_state(CustomSearching.series_length)
        await state.update_data(country=message.text)
        await message.answer(
            text="Напишите пожалуйста продолжительность серии или отрывок за который хотите осуществить поиск, например (40, 30-60)."
            "Вы так же можете пропустить этот этап нажав на кнопку 'Пропустить' ниже и тогда этот критерий не будет"
            "учитываться.",
            reply_markup=back_or_skip_kb(),
        )
    elif data["type_choice"] == "Фильмы и сериалы":
        data = await state.update_data(country=message.text)
        # TODO  # Доделать вывод на экран
    


@router.message(CustomSearching.country)
async def custom_searching_country_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Необходимо что бы вы написали страну(ы) которые хотите включить в рандомный поиск.",
        reply_markup=back_or_skip_kb(),
    )
