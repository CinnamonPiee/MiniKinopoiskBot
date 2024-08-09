from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from database.orm.user import (
    check_user_id_by_telegram_id,
    get_user_film_serial_history,
    get_user_film_serial_history_per_date)
from keyboards.inline.create_history_pagination_kb import create_pagination_kb
from keyboards.reply.main_kb import main_kb
from database.models import HistorySerial, HistoryFilm
from database.orm.film import get_user_film_history_per_date, get_user_film_history
from database.orm.serial import get_user_serial_history_per_date, get_user_serial_history
from utils.validations import Validations
from aiogram.types import FSInputFile

PER_PAGE = 1
router = Router(name=__name__)
