from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.login_registration_kb import login_registration
from states.registration import Registration
from utils.name_validation import name_validation


router = Router(name=__name__)


@router.message(Registration.name, F.text == "Назад")
async def registration_name_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.login_registration)
    await message.answer(
        text="Выберите что-нибудь одно."
        "Авторизуйтесь (если вы использовали браузерную"
        "версию приложения) или зарегистрируйтесь в боте."
        "Для регистрации необходимо ввести Юзернейм,"
        "Пароль, Почту и Номер телефона",
        reply_markup=login_registration(),
    )


@router.message(Registration.name, F.text.cast(name_validation).as_("name"))
async def registration_name_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.password)
    await state.update_data(name=message.text)
    await message.answer(
        text="Теперь введите пароль который вы указывали при регистрации"
             "в браузерной версии приложения: ",
        reply_markup=back_kb(),
        )


@router.message(Registration.name)
async def registration_name_handler_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю. Напишите пожалуйста ваше имя!",
        reply_markup=back_kb(),
        )

