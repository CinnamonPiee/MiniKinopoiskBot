from aiogram.fsm.state import State, StatesGroup


class HistoryOfSearch(StatesGroup):
    choose_film_serial_all = State()
    first_date = State()
    second_date = State()
