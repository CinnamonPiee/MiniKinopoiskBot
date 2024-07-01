import asyncio

from database.databases import async_session_factory
from models import Users

from sqlalchemy import select


class AsyncORM:
    @staticmethod
    async def insert_users():
        async with async_session_factory() as session:
            user_jack = Users(name="Jack",)
            user_michael = Users(name="Michael")
            session.add_all([user_michael, user_jack])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_users():
        async with async_session_factory() as session:
            query = select(Users)
            result = await session.execute(query)
            users = result.scalars().all()
            print(f"{users=}")


