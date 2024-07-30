from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.generation_password_back_kb import generation_password_back_kb
from states.registration import Registration
from utils.validations import Validations


router = Router(name=__name__)


@router.message(Registration.password, F.text == "Назад")
async def registration_password_back(message: Message, state: FSMContext):
    data = state.get_data()
    if data["login_registration"] == "Вход":
        await state.set_state(Registration.email)
        await message.answer(
            text="Введите вашу поту: ",
            reply_markup=back_kb(),
        )
    elif data["login_registration"] == "Регистрация":
        await state.get_state(Registration.name)
        await message.answer(
            text="Напишите пожалуйста ваш Никнейм: ",
            reply_markup=back_kb(),
        )


@router.message(Registration.password, F.text.cast(Validations.valid_password).as_("password"))
async def registration_password(message: Message, state: FSMContext):
    data = state.get_data()
    if data["login_registration"] == "Вход":
        # TODO # Доделать вариант если пользователь авторизовывается. Сделать проверку на 
        # правильно введенный пароль и если он правильный, то вывести приветсвенное окно и обновить
        # его карточку в бд с добавлением telegram_id
        pass
    elif data["login_registration"] == "Регистрация":
        await state.set_state(Registration.email)
        await state.update_data(password=message.text)
        await message.answer(
            text="Введите вашу почту: ",
            reply_markup=back_kb(),
        )


@router.message(Registration.password)
async def registration_password_none(message: Message):
    await message.answer(
        text="Простите, я вас не понял. Введите пожалуйста корректный пароль: "
             "1. Содержит только латинские буквы"
             "2. Не менее 8 символов"
             "3. Имеет хотя бы одну заглавную букву и одну цифру"
             "Вы так же можете сгенерировать безопасный пароль нажав "
             "на кнопку 'Сгенерировать пароль' ниже.",
        reply_markup=generation_password_back_kb(),
    )
