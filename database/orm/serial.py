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
        rating: float,
        release_year: str,
        series_length: str,
        country: str,
        age_rating: int,
        description: str,
        picture: str
        ):

    async with async_session_factory() as session:
        user = await session.execute(select(Users).filter_by(telegram_id=telegram_id))
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


async def update_search_history(user_id: int, serial_id: int):
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


async def add_search_history(user_id: int, serial_id: int):
    async with async_session_factory() as session:
        new_history = HistorySerial(
            user_id=user_id,
            film_id=serial_id,
            created_at=datetime.utcnow()
        )

        session.add(new_history)
        await session.commit()
