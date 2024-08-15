from sqlalchemy import text

from database.databases import async_session_factory


async def truncate_tables():
    async with async_session_factory() as session:
        async with session.begin():
            await session.execute(text(
                "TRUNCATE TABLE users_user RESTART IDENTITY CASCADE")
            )
            await session.execute(text(
                "TRUNCATE TABLE films_serials_searchfilm RESTART IDENTITY CASCADE")
            )
            await session.execute(text(
                "TRUNCATE TABLE films_serials_searchserial RESTART IDENTITY CASCADE")
            )
        await session.commit()
