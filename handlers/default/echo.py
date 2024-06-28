from aiogram.types import Message

from aiogram import Router


router = Router(name=__name__)


@router.message()
async def echo(message: Message) -> None:
    await message.reply(message.text)
