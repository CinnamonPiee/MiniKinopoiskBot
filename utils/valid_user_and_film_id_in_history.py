from database.models import SearchFilm, User, HistoryFilm
from database.orm.film import update_search_history, add_search_history
from database.databases import async_session_factory
from sqlalchemy.future import select


async def valid_user_and_film_id_in_history(name, telegram_id):
    async with async_session_factory() as session:
        result = await session.execute(select(SearchFilm).where(SearchFilm.name == name))
        existing_film = result.scalars().first()

        if existing_film:
            user_result = await session.execute(select(User).where(User.telegram_id == telegram_id))
            user = user_result.scalars().first()

            if user:
                data = await session.execute(select(HistoryFilm).where(
                    HistoryFilm.user_id == user.id, HistoryFilm.film_id == existing_film.id))
                data = data.scalars().first()

                if data:
                    await update_search_history(user.id, existing_film.id)
                else:
                    await add_search_history(user.id, existing_film.id)
