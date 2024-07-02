from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply.back_kb import back_kb
from states.registration import Registration
from utils.name_validation import name_validation


router = Router(name=__name__)


@router.message(Registration.name, F.text == "Назад")
async def registration_name_handler_back(message: Message, state: FSMContext):
    await message.answer(text="Для запуска бота используйте команду /start")
    await state.clear()


@router.message(Registration.name, F.text.cast(name_validation).as_("name"))
async def registration_name_handler(message: Message, state: FSMContext):
    await state.set_state(Registration.email)
    await state.update_data(name=message.text)
    await message.answer(
        text="Теперь введите пожалуйста свою почту: ",
        reply_markup=back_kb(),
        )


@router.message(Registration.name)
async def registration_name_handler_none(message: Message):
    await message.answer(
        text="Простите, я не понимаю. Напишите пожалуйста ваше имя!",
        reply_markup=back_kb(),
        )

