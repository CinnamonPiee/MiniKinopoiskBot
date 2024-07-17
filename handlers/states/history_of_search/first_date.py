from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.history_of_search import HistoryOfSearch
from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_today_kb import back_or_today_kb
from utils.date_valid import date_valid
from database.orm.user import (
    check_user_id_by_telegram_id,
    get_user_film_history,
    get_user_serial_history,
    get_user_film_serial_history)
from keyboards.inline.create_pagination_kb import create_pagination_kb
from utils.choice_film_serial_or_all import ChoiceFilmSerialOrAll
from database.models import HistoryFilm, HistorySerial

router = Router(name=__name__)
PER_PAGE = 1


@router.message(HistoryOfSearch.first_date, F.text == "Назад")
async def first_date_back(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.choose_film_serial_all)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=history_search_kb(),
    )


@router.message(HistoryOfSearch.first_date, F.text == "Пропустить")
async def first_date_skip(message: Message, state: FSMContext):
    choise_film_serial = await state.get_data()

    telegram_id = message.from_user.id
    user_id = await check_user_id_by_telegram_id(int(telegram_id))

    if choise_film_serial["choice"] == "Фильмы":
        ChoiceFilmSerialOrAll.choice = "Фильмы"
        if user_id:
            page = 0
            history, total_count = await get_user_film_history(user_id, page, PER_PAGE)
            if history:
                film = history[0].film
                keyboards = create_pagination_kb(page, total_count)
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=film.picture,
                    caption=f"{film.name}\n"
                            f"Жанры: {film.janr}\n"
                            f"Рейтинг: {film.rating}\n"
                            f"Год: {film.year}\n"
                            f"Продолжительность фильма: {film.movie_length}\n"
                            f"Страна: {film.country}\n"
                            f"Возрастной рейтинг: {film.age_rating}\n"
                            f"Описание: {film.description}",
                    reply_markup=keyboards,
                )
            else:
                await message.bot.send_message(
                    message.chat.id,
                    text="История поиска пуста.",
                    reply_markup=main_kb(),
                )
                await state.clear()
        await state.clear()

    elif choise_film_serial["choice"] == "Сериалы":
        ChoiceFilmSerialOrAll.choice = "Сериалы"
        if user_id:
            page = 0
            history, total_count = await get_user_serial_history(user_id, page, PER_PAGE)
            if history:
                serial = history[0].serial
                keyboards = create_pagination_kb(page, total_count)
                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=serial.picture,
                    caption=f"{serial.name}\n"
                            f"Жанры: {serial.janr}\n"
                            f"Рейтинг: {serial.rating}\n"
                            f"Релиз: {serial.release_year}\n"
                            f"Продолжительность серии: {serial.series_length}\n"
                            f"Страна: {serial.country}\n"
                            f"Возрастной рейтинг: {serial.age_rating}\n"
                            f"Описание: {serial.description}",
                    reply_markup=keyboards
                )
            else:
                await message.bot.send_message(
                    message.chat.id,
                    text="История поиска пуста.",
                    reply_markup=main_kb(),
                )
                await state.clear()
        await state.clear()

    # на проверке
    elif choise_film_serial["choice"] == "Фильмы и сериалы":
        ChoiceFilmSerialOrAll.choice = "Фильмы и сериалы"
        if user_id:
            page = 0
            history, total_count = await get_user_film_serial_history(user_id, page, PER_PAGE)
            if history:
                for item in history:
                    if isinstance(item, HistoryFilm):
                        film = item.film
                        keyboards = create_pagination_kb(page, total_count)
                        await message.bot.send_photo(
                            chat_id=message.chat.id,
                            photo=film.picture,
                            caption=f"{film.name}\n"
                                    f"Жанры: {film.janr}\n"
                                    f"Рейтинг: {film.rating}\n"
                                    f"Год: {film.year}\n"
                                    f"Продолжительность фильма: {film.movie_length}\n"
                                    f"Страна: {film.country}\n"
                                    f"Возрастной рейтинг: {film.age_rating}\n"
                                    f"Описание: {film.description}",
                            reply_markup=keyboards,
                        )
                    elif isinstance(item, HistorySerial):
                        serial = item.serial
                        keyboards = create_pagination_kb(page, total_count)
                        await message.bot.send_photo(
                            chat_id=message.chat.id,
                            photo=serial.picture,
                            caption=f"{serial.name}\n"
                                    f"Жанры: {serial.janr}\n"
                                    f"Рейтинг: {serial.rating}\n"
                                    f"Релиз: {serial.release_year}\n"
                                    f"Продолжительность серии: {serial.series_length}\n"
                                    f"Страна: {serial.country}\n"
                                    f"Возрастной рейтинг: {serial.age_rating}\n"
                                    f"Описание: {serial.description}",
                            reply_markup=keyboards
                        )
            else:
                await message.bot.send_message(
                    message.chat.id,
                    text="История поиска пуста.",
                    reply_markup=main_kb(),
                )
                await state.clear()
        await state.clear()


@router.message(HistoryOfSearch.first_date, F.text.cast(date_valid).as_("first_date"))
async def first_date(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.second_date)
    await state.update_data(first_date=message.text)
    await message.answer(
        text="Пожалуйста, введите конечную дату поиска (в формате ГГГГ-ММ-ДД)"
             " или нажмите на кнопку внизу для выбора сегодняшней даты.",
        reply_markup=back_or_today_kb(),
    )


@router.message(HistoryOfSearch.first_date)
async def first_date_skip_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
             "или нажмите на кнопку 'Пропустить' внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb(),
    )
