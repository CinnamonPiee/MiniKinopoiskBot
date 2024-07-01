from aiogram import Router

from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from states import (
    main_menu,
    find_film_serial,
    random_film_serial,
    low_coast_film_or_serial,
    height_coast_film_or_serial,
    custom_searching
)

from keyboards.reply import (
    main_kb,
    choose_criteries_kb,
    back_kb
)


router = Router(name=__name__)



