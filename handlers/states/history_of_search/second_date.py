from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from states.history_of_search import HistoryOfSearch

from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.back_kb import back_kb
from keyboards.inline.create_history_pagination_kb import create_history_pagination_kb
from keyboards.reply.main_kb import main_kb

from utils.validations import valid_date, valid_url

from database.orm.user import check_user_id_by_telegram_id, get_user_film_serial_history_per_date
from database.models import HistoryFilm, HistorySerial
from database.orm.film import get_user_film_history_per_date
from database.orm.serial import get_user_serial_history_per_date


router = Router(name=__name__)
PER_PAGE = 1


@router.message(HistoryOfSearch.second_date, F.text == "Назад")
async def second_date_back(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.first_date)
    await message.answer(
        text="Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
        "или нажмите на кнопку 'Пропустить' внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb(),
    )


@router.message(HistoryOfSearch.second_date, F.text.cast(valid_date.valid_date).as_("second_date"))
async def second_date(message: Message, state: FSMContext):
    await state.update_data(second_date=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id
    user_id = await check_user_id_by_telegram_id(int(telegram_id))

    if data["choice"] == "movie":
        if user_id:
            page = 0
            history, total_count = await get_user_film_history_per_date(
                user_id,
                page,
                PER_PAGE,
                str(data["first_date"]),
                str(data["second_date"])
            )
            if history:
                film = history[0].film

                if film.picture is not None and valid_url.valid_url(film.picture):
                    photo = film.picture
                else:
                    photo = FSInputFile(
                        "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                    )

                keyboards = create_history_pagination_kb(page, total_count)

                try:
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
                except:
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
                                f"Описание: None",
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

    elif data["choice"] == "tv-series":
        if user_id:
            page = 0
            history, total_count = await get_user_serial_history_per_date(
                user_id,
                page,
                PER_PAGE,
                str(data["first_date"]),
                str(data["second_date"])
            )
            if history:
                serial = history[0].serial

                if serial.picture is not None and valid_url.valid_url(serial.picture):
                    photo = serial.picture
                else:
                    photo = FSInputFile(
                        "/media/simon/MY FILES/Python/Bots/MiniKinopoiskBot/img/not-found-image-15383864787lu.jpg"
                    )

                keyboards = create_history_pagination_kb(page, total_count)

                try:
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
                except:
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
                                f"Описание: None",
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

    elif data["choice"] == None:
        if user_id:
            page = 0
            history, total_count = await get_user_film_serial_history_per_date(
                user_id,
                page,
                PER_PAGE,
                str(data["first_date"]),
                str(data["second_date"])
            )
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

                        try:
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
                        except:
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
                                        f"Описание: None",
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

                        try:
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
                        except:
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
                                        f"Описание: None",
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


@router.message(HistoryOfSearch.second_date)
async def second_date_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Пожалуйста, введите конечную дату поиска (в формате ГГГГ-ММ-ДД)",
        reply_markup=back_kb(),
    )
