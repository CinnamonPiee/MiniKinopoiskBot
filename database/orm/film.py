from sqlalchemy import func

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.databases import async_session_factory
from database.models import SearchFilm, HistoryFilm, User

from datetime import datetime
from datetime import timedelta


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
        user = await session.execute(
            select(User).filter_by(telegram_id=telegram_id)
        )

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


async def update_film_search_history(user_id: int, film_id: int):
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


async def add_film_search_history(user_id: int, film_id: int):
    async with async_session_factory() as session:
        new_history = HistoryFilm(
            user_id=user_id,
            film_id=film_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()


async def get_user_film_history(user_id: int, page: int, per_page: int):
    async with (async_session_factory() as session):
        query = select(
            HistoryFilm,
            SearchFilm
        ).options(
            joinedload(HistoryFilm.film)
        ).join(
            SearchFilm, HistoryFilm.film_id == SearchFilm.id
        ).where(
            HistoryFilm.user_id == user_id
        ).order_by(
            HistoryFilm.created_at.desc()
        ).limit(
            per_page
        ).offset(
            page * per_page
        )

        result = await session.execute(query)
        history = result.scalars().all()

        total_count = await session.scalar(
            select(func.count()).select_from(HistoryFilm).where(HistoryFilm.user_id == user_id)
        )

        return history, total_count


async def get_user_film_history_per_date(
        user_id: int, 
        page: int, 
        per_page: int, 
        first_date: str, 
        second_date: str
    ):
    async with async_session_factory() as session:
        start_date_dt = datetime.strptime(first_date, '%Y-%m-%d')
        end_date_dt = datetime.strptime(second_date, '%Y-%m-%d') + timedelta(days=1)

        query = select(
            HistoryFilm,
            SearchFilm
        ).options(
            joinedload(HistoryFilm.film)
        ).join(
            SearchFilm, HistoryFilm.film_id == SearchFilm.id
        ).where(
            HistoryFilm.user_id == user_id,
            HistoryFilm.created_at >= start_date_dt,
            HistoryFilm.created_at < end_date_dt
        ).order_by(
            HistoryFilm.created_at.desc()
        ).limit(
            per_page
        ).offset(
            page * per_page
        )

        result = await session.execute(query)
        history = result.scalars().all()

        total_count = await session.scalar(
            select(func.count()).select_from(HistoryFilm).where(
                HistoryFilm.user_id == user_id,
                HistoryFilm.created_at >= start_date_dt,
                HistoryFilm.created_at < end_date_dt
            )
        )

        return history, total_count
