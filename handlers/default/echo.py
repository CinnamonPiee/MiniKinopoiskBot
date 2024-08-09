from aiogram import Router

from aiogram.types import Message


router = Router(name=__name__)


@router.message()
async def echo(message: Message) -> None:
    await message.reply(message.text)
