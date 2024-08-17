from aiogram import Router, F

from aiogram.types import Message
from aiogram.filters import Command


router = Router(name=__name__)


@router.message(F.text == "Помощь ❓")
@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        text="/start - запустить бота или перейти в главное меню.\n"
             "/help - получить информацию по использованию бота.\n"
             "Бот для получения фильмов и сериалов по названию,"/
             "рандомно и через кастомный поиск. После регистрации"/
             "и авторизации в боте доступна история поиска."/
             "Навигация по боту доступна через кнопки под полем"/
             "ввода (в некоторых случаях через кнопки под сообщением)."/
             "Для того чтобы вернуться назад (выйти или изменить ввод)"/
             "всегда присутствует кнопка 'Назад' внизу под полем ввода."/
             "Приятного использования!"
    )
