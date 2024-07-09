from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.history_of_search import HistoryOfSearch
from keyboards.reply.history_search_kb import history_search_kb
from keyboards.reply.back_or_skip_kb import back_or_skip_kb
from keyboards.reply.back_kb import back_kb
from utils.date_valid import date_valid
from database.orm.user import check_user_by_telegram_id, get_user_film_history
from keyboards.inline import create_pagination_kb


router = Router(name=__name__)
PER_PAGE = 5


@router.message(HistoryOfSearch.first_date, F.text == "Назад")
async def first_date_back(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.choose_film_serial_all)
    await message.answer(
        text="Пожалуйста, выберите что вы хотите найти: ",
        reply_markup=history_search_kb(),
    )


@router.message(HistoryOfSearch.first_date, F.text == "Пропустить")
async def first_date_skip(message: Message):
    await message.answer(
        text="Вы выбрали историю за все время."
    )
    telegram_id = message.from_user.id
    user_id = await check_user_by_telegram_id(telegram_id)
    if user_id:
        page = 1
        history, total_count = await get_user_film_history(user_id, page, PER_PAGE)
        keyboards = create_pagination_kb(history, page, total_count)

        if history:
            for record in history:
                film = record.film
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
            await message.bot.send_message(message.chat.id, text="История поиска пуста.")
    else:
        await message.bot.send_message(message.chat.id, text="Пользователь не найден.")


@router.message(HistoryOfSearch.first_date, F.text.cast(date_valid).as_("first_date"))
async def first_date(message: Message, state: FSMContext):
    await state.set_state(HistoryOfSearch.second_date)
    await state.update_data(first_date=message.text)
    await message.answer(
        text="Пожалуйста, введите конечную дату поиска (в формате ГГГГ-ММ-ДД)",
        reply_markup=back_kb(),
    )


@router.message(HistoryOfSearch.first_date)
async def first_date_skip_none(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Пожалуйста, введите начальную дату поиска (в формате ГГГГ-ММ-ДД) "
        "или нажмите на кнопку <Пропустить> внизу чтобы просмотреть всю историю поиска.",
        reply_markup=back_or_skip_kb(),
        )
