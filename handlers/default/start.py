from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_kb import back_kb
from database.orm.user import check_user_by_telegram_id
from states.registration import Registration


router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if await check_user_by_telegram_id(int(message.from_user.id)):
        await message.answer(
            text=f"Привет, {message.from_user.first_name}!",
            reply_markup=main_kb(),
            )

    else:
        await state.set_state(Registration.name)
        await message.answer(
            text="Необходима регистрация в боте!\nНапишите пожалуйста ваше имя: ",
            reply_markup=back_kb(),
            )
