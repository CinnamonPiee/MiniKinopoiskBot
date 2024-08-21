from aiogram import Router, F

from aiogram.types import Message
from aiogram.utils import markdown

from keyboards.reply.main_kb import main_kb


router = Router(name=__name__)


@router.message(F.text == "Поддержка ⚙️")
async def support(message: Message):
    await message.answer(
        text=f"В случае возникновения проблем с ботом, можете\n" 
             f"написать в службу поддержки на почту support.minikinopoiskbot@gmail.com\n" 
             f"или написать нам в {markdown.hlink("телеграмм", "https://t.me/Simon_Sh1")}. Так же бот имеет\n" 
             f"открытый {markdown.hlink("исходный код", "https://github.com/CinnamonPiee/MiniKinopoiskBot")} и вы можете сами внести правки.",
        reply_markup=main_kb(),
    )
