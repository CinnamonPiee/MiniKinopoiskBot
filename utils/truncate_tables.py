from sqlalchemy import text

from database.databases import async_session_factory


async def truncate_tables():
    async with async_session_factory() as session:
        async with session.begin():
            await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE search_film RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE search_serial RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE history_search_film RESTART IDENTITY CASCADE"))
            await session.execute(text("TRUNCATE TABLE history_search_serial RESTART IDENTITY CASCADE"))
        await session.commit()
