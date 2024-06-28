from aiogram.types import Message
from aiogram.filters import Command

from aiogram import Router


router = Router(name=__name__)


@router.message(Command)
async def help_command(message: Message):
    await message.answer(text="Info about bot!")
