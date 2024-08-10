from sqlalchemy import func

from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from database.databases import async_session_factory
from database.models import SearchSerial, User, HistorySerial

from datetime import datetime
from datetime import timedelta


async def serial_exists(name: str) -> str | None:
    async with async_session_factory() as session:
        result = await session.execute(
            select(SearchSerial).where(SearchSerial.name == name)
        )
        serial = result.scalars().first()
        return serial is not None


async def add_serial(
        telegram_id: int,
        name: str,
        janr: str,
        rating: float,
        release_year: str,
        series_length: str,
        country: str,
        age_rating: int,
        description: str,
        picture: str
        ) -> None:
    async with async_session_factory() as session:
        user = await session.execute(select(User).filter_by(telegram_id=telegram_id))
        user = user.scalar_one_or_none()
        user_id = user.id

        new_serial = SearchSerial(
            name=name,
            janr=janr,
            rating=rating,
            release_year=release_year,
            series_length=series_length,
            country=country,
            age_rating=age_rating,
            description=description,
            picture=picture
        )

        session.add(new_serial)
        await session.commit()
        serial_id = new_serial.id

        new_history = HistorySerial(
            user_id=user_id,
            serial_id=serial_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()


async def update_serial_search_history(user_id: int, serial_id: int) -> None:
    async with async_session_factory() as session:
        result = await session.execute(
            select(HistorySerial).where(
                HistorySerial.user_id == user_id,
                HistorySerial.serial_id == serial_id
            )
        )

        existing_history = result.scalars().first()

        if existing_history:
            existing_history.created_at = datetime.utcnow()
            await session.commit()


async def add_serial_search_history(user_id: int, serial_id: int) -> None:
    async with async_session_factory() as session:
        new_history = HistorySerial(
            user_id=user_id,
            film_id=serial_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()


async def get_user_serial_history(
    user_id: int, 
    page: int, 
    per_page: int
) -> tuple[list[HistorySerial], int]:
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
            select(func.count()).select_from(HistorySerial).where(HistorySerial.user_id == user_id)
        )

        return history, total_count


async def get_user_serial_history_per_date(
    user_id: int, 
    page: int, 
    per_page: int, 
    first_date: str, 
    second_date: str
) -> tuple[list[HistorySerial], int]:
    async with async_session_factory() as session:
        start_date_dt = datetime.strptime(first_date, '%Y-%m-%d')
        end_date_dt = datetime.strptime(second_date, '%Y-%m-%d') + timedelta(days=1)

        query = select(
            HistorySerial,
            SearchSerial
        ).options(
            joinedload(HistorySerial.serial)
        ).join(
            SearchSerial, HistorySerial.serial_id == SearchSerial.id
        ).where(
            HistorySerial.user_id == user_id,
            HistorySerial.created_at >= start_date_dt,
            HistorySerial.created_at < end_date_dt
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
            select(func.count()).select_from(HistorySerial).where(
                HistorySerial.user_id == user_id,
                HistorySerial.created_at >= start_date_dt,
                HistorySerial.created_at < end_date_dt
            )
        )

        return history, total_count