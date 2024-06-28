from aiogram.fsm.state import StatesGroup, State


class FindFilmSerial(StatesGroup):
    name = State()
    janrs = State()
    count = State()