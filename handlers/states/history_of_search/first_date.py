from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from states.history_of_search import HistoryOfSearch

from keyboards.reply import (
    history_search_kb,
    back_or_today_kb,
    main_kb,
    back_or_skip_kb
)
from keyboards.inline.create_history_pagination_kb import create_history_pagination_kb

from database.orm.user import (check_user_id_by_telegram_id,get_user_film_serial_history)
from database.orm.film import get_user_film_history
from database.orm.serial import get_user_serial_history
from database.models import HistoryFilm, HistorySerial

from utils.validations import valid_url, valid_date


router = Router(name=__name__)
PER_PAGE = 1


@router.message(HistoryOfSearch.first_date, F.text == "Назад")
async def first_date_back(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.choose_film_serial_all)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=history_search_kb.history_search_kb(),
    )


@router.message(HistoryOfSearch.first_date, F.text == "Пропустить")
async def first_date_skip(message: Message, state: FSMContext):
    await state.update_data(first_date=None)
    await state.update_data(second_date=None)
    data = await state.get_data()
    telegram_id = message.from_user.id
    user_id = await check_user_id_by_telegram_id(int(telegram_id))

    if data["choice"] == "movie":
        if user_id:
            page = 0
            history, total_count = await get_user_film_history(user_id, page, PER_PAGE)
            if history:
                film = history[0].film

                if film.picture is not None and valid_url.valid_url(film.picture):
                    photo = film.picture
                else:
                    photo = FSInputFile(
                        "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                    )
            
                keyboards = create_history_pagination_kb(page, total_count)

                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
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
                    reply_markup=main_kb.main_kb(),
                )

                await state.clear()

    elif data["choice"] == "tv-series":
        if user_id:
            page = 0
            history, total_count = await get_user_serial_history(user_id, page, PER_PAGE)
            if history:
                serial = history[0].serial

                if serial.picture is not None and valid_url.valid_url(serial.picture):
                    photo = serial.picture
                else:
                    photo = FSInputFile(
                        "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                    )
                    
                keyboards = create_history_pagination_kb(page, total_count)

                await message.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
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
                    reply_markup=main_kb.main_kb(),
                )

                await state.clear()

    elif data["choice"] == None:
        if user_id:
            page = 0
            history, total_count = await get_user_film_serial_history(user_id, page, PER_PAGE)
            if history:
                for item in history:
                    if isinstance(item, HistoryFilm):
                        film = item.film

                        if film.picture is not None and valid_url.valid_url(film.picture):
                            photo = film.picture
                        else:
                            photo = FSInputFile(
                                "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                            )
                    
                        keyboards = create_history_pagination_kb(page, total_count)

                        await message.bot.send_photo(
                            chat_id=message.chat.id,
                            photo=photo,
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

                        if serial.picture is not None and valid_url.valid_url(serial.picture):
                            photo = serial.picture
                        else:
                            photo = FSInputFile(
                                "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                            )
                            
                        keyboards = create_history_pagination_kb(page, total_count)

                        await message.bot.send_photo(
                            chat_id=message.chat.id,
                            photo=photo,
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
                    reply_markup=main_kb.main_kb(),
                )
                
                await state.clear()


@router.message(HistoryOfSearch.first_date, F.text.cast(valid_date.valid_date).as_("first_date"))
async def first_date(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.second_date)
    await state.update_data(first_date=message.text)
    await message.answer(
        text="Пожалуйста, введите конечную дату поиска (в формате ГГГГ-ММ-ДД)"
             " или нажмите на кнопку внизу для выбора сегодняшней даты.",
        reply_markup=back_or_today_kb.back_or_today_kb(),
    )


@router.message(HistoryOfSearch.first_date)
async def first_date_skip_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
             "или нажмите на кнопку 'Пропустить' внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb.back_or_skip_kb(),
    )
