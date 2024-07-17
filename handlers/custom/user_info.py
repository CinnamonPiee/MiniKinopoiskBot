from aiogram import Router, F
from aiogram.types import Message
from config_data.config import settings
from utils.truncate_tables import truncate_tables


router = Router(name=__name__)


@router.message(F.text == "user_info")
async def user_info(message: Message):
    await message.answer(text=str(message.from_user.id))
