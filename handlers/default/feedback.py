from aiogram import Router, F

from aiogram.types import Message
from aiogram.utils import markdown

from keyboards.reply.main_kb import main_kb


router = Router(name=__name__)


@router.message(F.text == "Обратная связь 📧")
async def feedback(message: Message):
    await message.answer(
        text=f"Почта - {markdown.hlink("support.minikinopoiskbot@gmail.com", 
                                       "support.minikinopoiskbot@gmail.com")}\n"
        f"Телеграмм - {markdown.hlink("https://t.me/Simon_Sh1", "https://t.me/Simon_Sh1")}\n" 
        f"GitHub - {markdown.hlink("https://github.com/CinnamonPiee/MiniKinopoiskBot",
                                        "https://github.com/CinnamonPiee/MiniKinopoiskBot")}",
        reply_markup=main_kb(),
    )
