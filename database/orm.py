from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import update, delete
from .databases import async_session_factory


async def check_user_by_telegram_id(telegram_id: int):
    from .models import Users
    async with async_session_factory() as session:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user is not None


async def get_user_by_id(user_id: int):
    from .models import Users
    async with async_session_factory() as session:
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalars().first()
        return user


async def get_users():
    from .models import Users
    async with async_session_factory() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return users


async def get_films():
    from .models import SearchFilm
    async with async_session_factory() as session:
        result = await session.execute(select(SearchFilm))
        films = result.scalars().all()
        return films


async def add_user(name: str, email: str, phone_number: str, telegram_id: int):
    from .models import Users
    async with async_session_factory() as session:
        new_user = Users(
            name=name,
            email=email,
            phone_number=phone_number,
            telegram_id=telegram_id,
            created_at=datetime.utcnow()
        )
        session.add(new_user)
        await session.commit()


async def update_user(user_id: int, **kwargs):
    from .models import Users
    async with async_session_factory() as session:
        await session.execute(
            update(Users).where(Users.id == user_id).values(**kwargs)
        )
        await session.commit()


async def delete_user(user_id: int):
    from .models import Users
    async with async_session_factory() as session:
        await session.execute(
            delete(Users).where(Users.id == user_id)
        )
        await session.commit()


async def add_film(
        user_id: int,
        name: str,
        janr: str,
        year: int,
        box_office: float,
        country: str,
        description: str,
        rating: float,
        ):
    from .models import SearchFilm, History
    async with async_session_factory() as session:
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

        new_history = History(
            user_id=user_id,
            film_id=film_id,
            created_at=datetime.utcnow()
        )
        session.add(new_history)
        await session.commit()
