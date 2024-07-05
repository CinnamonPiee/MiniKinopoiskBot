from database.models import SearchSerial, Users, HistorySerial
from database.orm.serial import update_search_history, add_search_history
from database.databases import async_session_factory
from sqlalchemy.future import select


async def valid_user_and_serial_id_in_history(name, telegram_id):
    async with async_session_factory() as session:
        result = await session.execute(select(SearchSerial).where(SearchSerial.name == name))
        existing_serial = result.scalars().first()

        if existing_serial:
            user_result = await session.execute(select(Users).where(Users.telegram_id == telegram_id))
            user = user_result.scalars().first()

            if user:
                data = await session.execute(select(HistorySerial).where(
                    HistorySerial.user_id == user.id, HistorySerial.serial_id == existing_serial.id))
                data = data.scalars().first()

                if data:
                    await update_search_history(user.id, existing_serial.id)
                else:
                    await add_search_history(user.id, existing_serial.id)
