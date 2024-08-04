from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from states.registration import Registration


router = Router(name=__name__)


@router.message(Registration.login_registration, F.text == "Назад")
async def registration_login_registration_handler_back(message: Message, state: FSMContext):
    await message.answer(text="Для запуска бота используйте команду /start")
    await state.clear()


@router.message(Registration.login_registration, F.text == "Вход")
async def registration_login_handler(message: Message, state: FSMContext):
    await state.update_data(login_registration=message.text)
    await state.set_state(Registration.email)
    await message.answer(
        text="Введите вашу поту: ",
        reply_markup=back_kb(),
    )


@router.message(Registration.login_registration, F.text == "Регистрация")
async def registration_registration_handler(message: Message, state: FSMContext):
    await state.update_data(login_registration=message.text)
    await state.set_data(Registration.name)
    await message.answer(
        text="Напишите пожалуйста ваш Никнейм: ",
        reply_markup=back_kb(),
    )


@router.message(Registration.login_registration)
async def registration_login_registration(message: Message):
    await message.answer(
        text="Простите, я вас не понимаю. Выберите пожалуйста вход или регистрация",
    )
