from database.models import SearchFilm, Users
from database.orm.film import update_search_history
from database.databases import async_session_factory
from sqlalchemy.future import select


async def valid_user_and_film_id_in_history(name, telegram_id):
    async with async_session_factory() as session:
        result = await session.execute(select(SearchFilm).where(SearchFilm.name == name))
        existing_film = result.scalars().first()
        if existing_film:
            user_result = await session.execute(select(Users).where(Users.telegram_id == telegram_id))
            user = user_result.scalars().first()
            if user:
                await update_search_history(user.id, existing_film.id)
