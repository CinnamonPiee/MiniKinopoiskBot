from aiogram.fsm.state import State, StatesGroup


class HistoryOfSearch(StatesGroup):
    first_date = State()
    second_date = State()
