from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.back_kb import back_kb
from keyboards.reply.login_registration_kb import login_registration_kb

from states.registration import Registration

from utils.validations.valid_name import valid_name


router = Router(name=__name__)


@router.message(Registration.name, F.text == "Назад")
async def registration_name_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.login_registration)
    
    await message.answer(
        text="Выберите что-нибудь одно."
        "Авторизуйтесь или зарегистрируйтесь в боте."
        "Для регистрации необходимо ввести Юзернейм,"
        "Пароль, Почту и Номер телефона",
        reply_markup=login_registration_kb(),
    )


@router.message(Registration.name, F.text.cast(valid_name).as_("name"))
async def registration_name_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.password)
    await state.update_data(name=message.text)

    await message.answer(
        text="Придумайте пароль: "
             "1. Содержит только латинские буквы"
             "2. Не менее 8 символов"
             "3. Имеет хотя бы одну заглавную букву и одну цифру"
             "Вы так же можете сгенерировать безопасный пароль нажав "
             "на кнопку 'Сгенерировать пароль' ниже.",
        reply_markup=back_kb(),
    )


@router.message(Registration.name)
async def registration_name_handler_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю. Напишите пожалуйста ваше имя!",
        reply_markup=back_kb(),
        )

