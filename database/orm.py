from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import update
from databases import async_session_factory


async def check_user_by_telegram_id(telegram_id: int):
    from models import Users  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user is not None


async def get_user_by_id(user_id: int):
    from models import Users  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalars().first()
        return user


# Пример асинхронной функции для получения данных о пользователях
async def get_users():
    from models import Users  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return users


# Пример асинхронной функции для получения данных о фильмах
async def get_films():
    from models import SearchFilm  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        result = await session.execute(select(SearchFilm))
        films = result.scalars().all()
        return films


# Пример асинхронной функции для получения истории поиска
async def get_history():
    from models import History  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        result = await session.execute(select(History))
        history = result.scalars().all()
        return history


# Пример асинхронной функции для добавления нового пользователя
async def add_user(name: str, email: str, phone_number: str, telegram_id: int):
    from models import Users  # Импорт перемещен внутрь функции
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


# Пример асинхронной функции для обновления данных о пользователе
async def update_user(user_id: int, **kwargs):
    from models import Users  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        await session.execute(
            update(Users).where(Users.id == user_id).values(**kwargs)
        )
        await session.commit()


# Пример асинхронной функции для добавления записи в историю поиска
async def add_search_history(user_id: int, film_id: int):
    from models import History  # Импорт перемещен внутрь функции
    async with async_session_factory() as session:
        new_history = History(
            user_id=user_id,
            film_id=film_id,
            created_at=datetime.utcnow()
        )
        session.add(new_history)
        await session.commit()
