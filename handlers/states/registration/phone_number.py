from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.back_kb import back_kb
from keyboards.reply.main_kb import main_kb
from states.registration import Registration


router = Router(name=__name__)


@router.message(Registration.phone_number, F.text == "Назад")
async def registration_phone_number_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.email)
    await message.answer(
        text="Напишите пожалуйста вашу почту: ",
        reply_markup=back_kb(),
        )


@router.message(Registration.phone_number, F.contact)
async def registration_phone_number_handler(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
        await message.answer(
            text="Спасибо за регистрацию в боте. Теперь вы можете пользоваться всем функционалом бота.",
            reply_markup=main_kb(),
        )
        await state.clear()


@router.message(Registration.phone_number)
async def registration_phone_number_handler_none(message: Message):
    await message.answer(
        text="Простите я не понимаю. Нажмите на кнопку <Поделиться контактом> для отправки вашего номера телефона.",
    )

