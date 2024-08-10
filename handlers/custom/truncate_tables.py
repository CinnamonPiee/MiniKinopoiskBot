from aiogram import Router, F

from aiogram.types import Message

from config_data.config import settings

from utils.truncate_tables import truncate_tables


router = Router(name=__name__)


@router.message(F.from_user.id.in_({42, int(settings.admin_id)}), F.text == "truncate table")
async def handle_truncate_command(message: Message):
    await truncate_tables()
    await message.answer(
        text="All tables have been truncated."
    )
