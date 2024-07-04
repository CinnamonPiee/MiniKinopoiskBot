from datetime import datetime
from sqlalchemy.future import select
from database.databases import async_session_factory
from database.models import SearchSerial, Users, HistorySerial


async def get_serials():
    async with async_session_factory() as session:
        result = await session.execute(select(SearchSerial))
        serial = result.scalars().all()
        return serial


async def serial_exists(name: str):
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
        release_year: str,
        series_length: str,
        country: str,
        description: str,
        rating: float
        ):

    async with async_session_factory() as session:
        user = await session.execute(select(Users).filter_by(telegram_id=telegram_id))
        user = user.scalar_one_or_none()
        user_id = user.id

        new_serial = SearchSerial(
            name=name,
            janr=janr,
            release_year=release_year,
            series_length=series_length,
            country=country,
            description=description,
            rating=rating
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
