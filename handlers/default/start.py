from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram import Router

from keyboards.reply.main_kb import main_kb


router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        text=f"Привет, {message.from_user.first_name}!",
        reply_markup=main_kb(),
        )
