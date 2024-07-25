from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.reply.back_kb import back_kb
from keyboards.reply.login_registration_kb import login_registration
from states.registration import Registration
from utils.name_validation import name_validation


router = Router(name=__name__)


TODO # Доделать пароль с вариацией если пользователь авторизовывается или регистрируется