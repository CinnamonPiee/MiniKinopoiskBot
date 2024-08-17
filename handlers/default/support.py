from aiogram import Router, F

from aiogram.types import Message
from aiogram.utils import markdown


router = Router(name=__name__)


@router.message(F.text == "Поддержка ⚙️")
async def support(message: Message):
    await message.answer(
        text=f"В случае возникновения пробоем с ботом, можете"/
             f"написать в службу поддержки на {markdown.hlink("почту", "support.minikinopoiskbot@gmail.com")}"/
             f"или написать нам в {markdown("телеграмм", "https://t.me/Simon_Sh1")}. Так же бот имеет"/
             f"открытый {"исходный код", "https://github.com/CinnamonPiee/MiniKinopoiskBot"} и вы можете сами внести правки."
    )
