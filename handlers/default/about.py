from aiogram import Router, F

from aiogram.types import Message
from aiogram.utils import markdown


router = Router(name=__name__)


@router.message(F.text == "О боте ❗️")
async def about(message: Message):
    await message.answer(
        text="Бот который помогает искать фильмы и сериалы\n"
             "по названию, рандомно и через кастомный поиск."
    )