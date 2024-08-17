from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.back_kb import back_kb
from keyboards.reply.main_kb import main_kb

from states.registration import Registration

from utils.validations.valid_password import valid_password

from database.orm.user import verify_user_password, update_telegram_id_by_email



router = Router(name=__name__)


@router.message(Registration.password, F.text == "🚫 Назад 🚫")
async def registration_password_back(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["login_registration"] == "Вход 🔑":
        await state.set_state(Registration.email)
        await message.answer(
            text="Введите вашу поту. ",
            reply_markup=back_kb(),
        )

    elif data["login_registration"] == "Регистрация 💯":
        await state.set_state(Registration.name)
        await message.answer(
            text="Напишите ваш Никнейм. ",
            reply_markup=back_kb(),
        )


@router.message(Registration.password, F.text.cast(valid_password).as_("password"))
async def registration_password(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["login_registration"] == "Вход 🔑":

        if await verify_user_password(data["email"], message.text):
            await update_telegram_id_by_email(data["email"], int(message.from_user.id))
            await message.answer(
                text=f"Добро пожаловать, {message.from_user.first_name}!",
                reply_markup=main_kb(),
            )

            await state.clear()

        else:
            await message.answer(
                text="Неверный пароль! Повторите попытку.",
                reply_markup=back_kb(),
            )

    elif data["login_registration"] == "Регистрация 💯":
        await state.set_state(Registration.email)
        await state.update_data(password=message.text)
        await message.answer(
            text="Введите вашу почту. ",
            reply_markup=back_kb(),
        )


@router.message(Registration.password)
async def registration_password_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял.😔\n"
             "Введите пожалуйста корректный пароль:\n"
             "1. Содержит только латинские буквы\n"
             "2. Не менее 8 символов\n"
             "3. Имеет хотя бы одну заглавную букву и одну цифру",
        reply_markup=back_kb(),
    )
