from aiogram.fsm.state import StatesGroup, State


class HeightCoastFilmSerial(StatesGroup):
    criteries_yes_or_no = State()
    janr = State()
    year = State()
    country = State()
