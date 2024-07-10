import logging
import asyncio

from config_data.config import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import router as main_router
from handlers.callbacks.change_page_callback_handler import change_page_callback_handler


async def main():
    dp = Dispatcher()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    logging.basicConfig(level=logging.INFO)

    dp.include_routers(main_router)

    # Зарегистрируйте обработчик
    dp.callback_query.register(change_page_callback_handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
