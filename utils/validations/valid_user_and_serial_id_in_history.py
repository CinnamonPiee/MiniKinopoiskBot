from database.models import SearchSerial, HistorySerial, User
from database.databases import async_session_factory
from database.orm.serial import update_serial_search_history, add_serial_search_history

from sqlalchemy.future import select


async def valid_user_and_serial_id_in_history(name: str, telegram_id: int):
    async with async_session_factory() as session:
        result = await session.execute(
            select(SearchSerial).where(SearchSerial.name == name)
        )
        
        existing_serial = result.scalars().first()

        if existing_serial:
            user_result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )

            user = user_result.scalars().first()

            if user:
                data = await session.execute(select(HistorySerial).where(
                    HistorySerial.user_id == user.id, 
                    HistorySerial.serial_id == existing_serial.id)
                )

                data = data.scalars().first()

                if data:
                    await update_serial_search_history(user.id, existing_serial.id)
                else:
                    await add_serial_search_history(user.id, existing_serial.id)
