from datetime import datetime
from sqlalchemy import update, delete
from sqlalchemy.future import select
from database.databases import async_session_factory
from database.models import Users


async def get_users():
    async with async_session_factory() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return users


async def get_user_by_id(user_id: int):
    async with async_session_factory() as session:
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalars().first()
        return user


async def check_user_by_telegram_id(telegram_id: int):
    async with async_session_factory() as session:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user is not None


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
