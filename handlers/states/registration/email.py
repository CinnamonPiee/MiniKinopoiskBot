from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_number_kb import back_or_number_kb
from states.registration import Registration
from utils.email_validation import email_validation
from database.orm.user import email_exists
from keyboards.reply.registration_kb import registration_kb
from keyboards.reply.login_registration_kb import login_registration_kb
from keyboards.reply.generation_password_back_kb import generation_password_back_kb


router = Router(name=__name__)


@router.message(Registration.email, F.text == "Назад")
async def registration_email_handler_back(message: Message, state: FSMContext):
    data = state.get_data()
    if data["login_registration"] == "Вход":
        await state.set_state(Registration.login_registration)
        await message.answer(
            text="Авторизуйтесь или зарегистрируйтесь в боте."
                 "Для регистрации необходимо ввести Юзернейм,"
                 "Пароль, Почту и Номер телефона",
            reply_markup=login_registration_kb(),
            )
    elif data["login_registration"] == "Регистрация":
        await state.set_state(Registration.password)
        await message.answer(
            text="Придумайте пароль: "
            "1. Содержит только латинские буквы"
            "2. Не менее 8 символов"
            "3. Имеет хотя бы одну заглавную букву и одну цифру"
            "Вы так же можете сгенерировать безопасный пароль нажав "
            "на кнопку 'Сгенерировать пароль' ниже.",
            reply_markup=generation_password_back_kb(),
        )


@router.message(Registration.email, F.text.cast(email_validation).as_("email"))
async def registration_email_handler(message: Message, state: FSMContext):
    data = state.get_data()
    if data["login_registration"] == "Вход":
        if await email_exists(message.text):
            await state.set_state(Registration.password)
            await message.answer(
                text="Теперь введите пароль: ",
                reply_markup=back_kb(),
                parse_mode=None,
                )
        else:
            await message.answer(
                text="Данная почта не найдена в базе данных, пожалуйста введите корректную почту"
                     " или зарегистрируйтесь в боте!",
                reply_markup=back_kb(),
            )

    elif data["login_registration"] == "Регистрация":
        if await email_exists(message.text):
            await message.answer(
                text="Данная почта уже есть в базе данных, можете попробовать авторизоваться"
                     "или попробуйте ввести другую почту.",
                reply_markup=registration_kb(),
            )
        else:
            await state.update_data(email=message.text)
            await state.set_state(Registration.phone_number)
            await message.answer(
                text="Теперь мне надо узнать ваш номер телефона. Для этого нажмите на кнопку <Поделиться номером> снизу. ",
                reply_markup=back_or_number_kb(),
                parse_mode=None,
                )


@router.message(Registration.email)
async def registration_email_handler_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю. Напишите пожалуйста корректную почту!",
        reply_markup=back_kb(),
    )
