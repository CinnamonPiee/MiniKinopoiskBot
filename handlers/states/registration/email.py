from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.back_or_number_kb import back_or_number_kb
from states.registration import Registration
from utils.email_validation import email_validation


router = Router(name=__name__)


@router.message(Registration.email, F.text == "Назад")
async def registration_email_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer(
        text="Напишите пожалуйста ваше имя: ",
        reply_markup=back_kb(),
        )


@router.message(Registration.email, F.text.cast(email_validation).as_("email"))
async def registration_email_handler(message: Message, state: FSMContext):
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
