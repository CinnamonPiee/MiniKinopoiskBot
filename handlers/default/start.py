from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram import Router


router = Router(name=__name__)


@router.message(CommandStart)
async def start_command(message: Message):
    await message.answer(text=f"Hello, {message.from_user.first_name}!")
