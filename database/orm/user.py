from datetime import datetime
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.databases import async_session_factory
from database.models import Users, HistoryFilm, SearchFilm, HistorySerial, SearchSerial
from sqlalchemy import func


async def get_users():
    async with async_session_factory() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return users


async def check_user_by_telegram_id(telegram_id: int):
    async with async_session_factory() as session:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user


async def check_user_id_by_telegram_id(telegram_id: int):
    async with async_session_factory() as session:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return int(user.id)


async def add_user(name: str,
                   email: str,
                   phone_number: str,
                   telegram_id: int
                   ):

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
    async with async_session_factory() as session:
        await session.execute(
            update(Users).where(Users.id == user_id).values(**kwargs)
        )

        await session.commit()


async def delete_user(user_id: int):
    async with async_session_factory() as session:
        await session.execute(
            delete(Users).where(Users.id == user_id)
        )

        await session.commit()


async def email_exists(email: str) -> bool:
    async with async_session_factory() as session:
        result = await session.execute(
            select(Users).where(Users.email == email)
        )
        user = result.scalars().first()
        return user is not None


async def phone_number_exists(phone_number: str) -> bool:
    async with async_session_factory() as session:
        result = await session.execute(
            select(Users).where(Users.phone_number == phone_number)
        )
        user = result.scalars().first()
        return user is not None


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
            select(func.count()).select_from(HistoryFilm).where(HistoryFilm.user_id == user_id))

        return history, total_count


async def get_user_serial_history(user_id: int, page: int, per_page: int):
    async with (async_session_factory() as session):
        query = select(
            HistorySerial,
            SearchSerial
        ).options(
            joinedload(HistorySerial.serial)
        ).join(
            SearchSerial, HistorySerial.serial_id == SearchSerial.id
        ).where(
            HistorySerial.user_id == user_id
        ).order_by(
            HistorySerial.created_at.desc()
        ).limit(
            per_page
        ).offset(
            page * per_page
        )

        result = await session.execute(query)
        history = result.scalars().all()
        total_count = await session.scalar(
            select(func.count()).select_from(HistorySerial).where(HistorySerial.user_id == user_id))

        return history, total_count


async def get_user_film_serial_history(user_id: int, page: int, per_page: int):
    async with async_session_factory() as session:
        # Get film history
        film_query = select(
            HistoryFilm
        ).options(
            joinedload(HistoryFilm.film)
        ).where(
            HistoryFilm.user_id == user_id
        ).order_by(
            HistoryFilm.created_at.desc()
        )

        film_result = await session.execute(film_query)
        film_history = film_result.scalars().all()

        # Get serial history
        serial_query = select(
            HistorySerial
        ).options(
            joinedload(HistorySerial.serial)
        ).where(
            HistorySerial.user_id == user_id
        ).order_by(
            HistorySerial.created_at.desc()
        )

        serial_result = await session.execute(serial_query)
        serial_history = serial_result.scalars().all()

        # Combine both histories
        combined_history = sorted(
            film_history + serial_history,
            key=lambda x: x.created_at,
            reverse=True
        )

        # Paginate combined history
        start_index = page * per_page
        end_index = start_index + per_page
        paginated_history = combined_history[start_index:end_index]

        # Get total count for pagination
        total_count = len(combined_history)

        return paginated_history, total_count
