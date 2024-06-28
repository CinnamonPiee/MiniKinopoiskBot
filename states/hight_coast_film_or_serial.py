from aiogram.fsm.state import StatesGroup, State


class LowCoastFilmSerial(StatesGroup):
    criteries_yes_or_no = State()
    janr = State()
    year = State()
    country = State()
