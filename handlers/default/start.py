from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router
from keyboards.reply.login_registration_kb import login_registration_kb
from keyboards.reply.back_kb import back_kb
from keyboards.reply.main_kb import main_kb
from states.registration import Registration
from database.orm.user import check_user_by_telegram_id



router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if await check_user_by_telegram_id(int(message.from_user.id)):
        await message.answer(
            text=f"Привет, {message.from_user.first_name}!",
            reply_markup=main_kb(),
        )
    else:
        await state.set_state(Registration.login_registration)
        await message.answer(
            text=f"Привет, {message.from_user.first_name}!"
                  "Авторизуйтесь (если вы использовали браузерную"
                  "версию приложения) или зарегистрируйтесь в боте."
                  "Для регистрации необходимо ввести Юзернейм,"
                  "Почту, Пароль и Номер телефона",
            reply_markup=login_registration_kb(),
            )    
