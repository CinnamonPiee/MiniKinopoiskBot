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
        box_office: float,
        country: str,
        description: str,
        rating: float,
        ):

    async with async_session_factory() as session:
        user = await session.execute(select(Users).filter_by(telegram_id=telegram_id))
        user = user.scalar_one_or_none()
        user_id = user.id

        new_film = SearchFilm(
            name=name,
            janr=janr,
            year=year,
            box_office=box_office,
            country=country,
            description=description,
            rating=rating
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
