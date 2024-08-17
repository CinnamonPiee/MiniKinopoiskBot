from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.login_registration_kb import login_registration_kb
from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_number_kb import back_or_number_kb

from states.registration import Registration

from utils.validations.valid_email import valid_email

from database.orm.user import email_exists


router = Router(name=__name__)


@router.message(Registration.email, F.text == "🚫 Назад 🚫")
async def registration_email_handler_back(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["login_registration"] == "Вход 🔑":
        await state.set_state(Registration.login_registration)
        await message.answer(
            text="Войдите или зарегистрируйтесь в боте.",
            reply_markup=login_registration_kb(),
            )
        
    elif data["login_registration"] == "Регистрация 💯":
        await state.set_state(Registration.password)
        await message.answer(
            text="Придумайте пароль:\n"
                 "1. Содержит только латинские буквы\n"
                 "2. Не менее 8 символов\n"
                 "3. Имеет хотя бы одну заглавную букву и одну цифру\n",
            reply_markup=back_kb(),
        )


@router.message(Registration.email, F.text.cast(valid_email).as_("email"))
async def registration_email_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["login_registration"] == "Вход 🔑":
        if await email_exists(message.text):
            await state.set_state(Registration.password)
            await state.update_data(email=message.text)
            await message.answer(
                text="Теперь введите пароль. ",
                reply_markup=back_kb(),
                parse_mode=None,
            )
            
        else:
            await message.answer(
                text="Данная почта не найдена.\n"
                     "Пожалуйста, повторите попытку\n"
                     "или зарегистрируйтесь в боте!",
                reply_markup=back_kb(),
            )

    elif data["login_registration"] == "Регистрация 💯":
        if await email_exists(message.text):
            await message.answer(
                text="Данная почта уже используется!\n"
                     "Можете попробовать авторизоваться\n"
                     "или попробуйте ввести другую почту.",
                reply_markup=back_kb(),
            )

        else:
            await state.update_data(email=message.text)
            await state.set_state(Registration.phone_number)
            await message.answer(
                text="Теперь введите ваш номер телефона\n"
                     "или нажмите на кнопку <Поделиться номером> ⬇️.",
                reply_markup=back_or_number_kb(),
                parse_mode=None,
            )


@router.message(Registration.email)
async def registration_email_handler_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю.😔\n"
             "Напишите корректную почту!",
        reply_markup=back_kb(),
    )
