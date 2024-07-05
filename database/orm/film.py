from datetime import datetime
from sqlalchemy.future import select
from database.databases import async_session_factory
from database.models import SearchFilm, HistoryFilm, Users


async def get_films():
    async with async_session_factory() as session:
        result = await session.execute(select(SearchFilm))
        films = result.scalars().all()
        return films


async def film_exists(name: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(SearchFilm).where(SearchFilm.name == name)
        )

        film = result.scalars().first()
        return film is not None


async def add_film(
        telegram_id: int,
        name: str,
        janr: str,
        year: int,
        country: str,
        movie_length: int,
        description: str,
        rating: float,
        age_rating: int,
        picture: str
        ):

    async with async_session_factory() as session:
        user = await session.execute(select(Users).filter_by(telegram_id=telegram_id))
        user = user.scalar_one_or_none()
        user_id = user.id

        new_film = SearchFilm(
            name=name,
            janr=janr,
            year=year,
            country=country,
            movie_length=movie_length,
            description=description,
            rating=rating,
            age_rating=age_rating,
            picture=picture
        )

        session.add(new_film)
        await session.commit()
        film_id = new_film.id

        new_history = HistoryFilm(
            user_id=user_id,
            film_id=film_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()


async def update_search_history(user_id: int, film_id: int):
    async with async_session_factory() as session:
        result = await session.execute(
            select(HistoryFilm).where(
                HistoryFilm.user_id == user_id,
                HistoryFilm.film_id == film_id
            )
        )
        existing_history = result.scalars().first()

        if existing_history:
            existing_history.created_at = datetime.utcnow()
            await session.commit()


async def add_search_history(user_id: int, film_id: int):
    async with async_session_factory() as session:
        new_history = HistoryFilm(
            user_id=user_id,
            film_id=film_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()
