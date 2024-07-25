from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_number_kb import back_or_number_kb
from states.registration import Registration
from utils.email_validation import email_validation
from database.orm.user import email_exists
from keyboards.reply.registration_kb import registration_kb


router = Router(name=__name__)

TODO # Сделать вариацию если пользователь авторизовывается или регистрируется
@router.message(Registration.email, F.text == "Назад")
async def registration_email_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.password)
    await message.answer(
        text="Теперь введите пароль который вы указывали при регистрации"
             "в браузерной версии приложения: ",
        reply_markup=back_kb(),
        )


@router.message(Registration.email, F.text.cast(email_validation).as_("email"))
async def registration_email_handler(message: Message, state: FSMContext):
    email = message.text
    data = state.get_data()
    if data["login_registration"] == "Вход":
        if await email_exists(email):
            await state.update_data(email=message.text)
            await state.set_state(Registration.password)
            await message.answer(
                text="Теперь введите пароль который вы указывали при регистрации"
                     "в браузерной версии приложения: ",
                reply_markup=back_kb(),
                parse_mode=None,
                )
        else:
            await message.answer(
                text="Данная почта не найдена в базе данных, пожалуйста введите корректную почту"
                     " или зарегистрируйтесь в боте!",
                reply_markup=registration_kb(),
            )
    elif data["login_registration"] == "Регистрация":
        if await email_exists(email):
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
