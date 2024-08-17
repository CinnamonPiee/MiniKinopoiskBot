from aiogram import Router

from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.reply.main_kb import main_kb
from keyboards.reply.login_registration_kb import login_registration_kb

from states.registration import Registration

from database.orm.user import check_user_by_telegram_id



router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if await check_user_by_telegram_id(message.from_user.id):
        await message.answer(
            text=f"Привет, {message.from_user.first_name}!",
            reply_markup=main_kb(),
        )
    else:
        await state.set_state(Registration.login_registration)
        await message.answer(
            text=f"Добро пожаловать, {message.from_user.username}!\n"
                  "Войдите или зарегистрируйтесь в боте.",
            reply_markup=login_registration_kb(),
        )    
