from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.back_kb import back_kb
from keyboards.reply.main_kb import main_kb
from keyboards.reply.back_or_number_kb import back_or_number_kb

from states.registration import Registration

from utils.validations.valid_phonenumber import valid_phonenumber

from database.orm.user import add_user, phone_number_exists


router = Router(name=__name__)


@router.message(Registration.phone_number, F.text == "Назад")
async def registration_phone_number_handler_back(message: Message, state: FSMContext):
    await state.set_state(Registration.email)
    await message.answer(
        text="Напишите пожалуйста вашу почту: ",
        reply_markup=back_kb(),
    )


@router.message(Registration.phone_number, 
    F.text.cast(valid_phonenumber).as_("phone_number") or F.contact)
async def registration_phone_number_handler(message: Message, state: FSMContext):
    if await phone_number_exists(message.text):
        await message.answer(
            text="Этот номер телефона уже зарегистрирован. Пожалуйста, используйте другой номер телефона.",
            reply_markup=back_or_number_kb(),
            parse_mode=None,
        )
    
    if message.contact.phone_number:
        await state.update_data(phone_number=str(message.contact.phone_number))
    else:
        await state.update_data(phone_number=message.text)

    data = await state.get_data()

    await add_user(
        password=data["password"],
        username=data["name"],
        email=data["email"],
        telegram_id=int(message.from_user.id),
        phone_number=data["phone_number"],
    )
    
    await message.answer(
        text="Спасибо за регистрацию в боте. Теперь вы можете пользоваться всем функционалом бота.",
        reply_markup=main_kb(),
        parse_mode=None,
    )

    await state.clear()


@router.message(Registration.phone_number)
async def registration_phone_number_handler_none(message: Message):
    await message.answer(
        text="Простите я не понимаю. Нажмите на кнопку <Поделиться номером> для отправки вашего номера телефона.",
        reply_markup=back_or_number_kb(),
        parse_mode=None,
    )

