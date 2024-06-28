from aiogram.fsm.state import State, StatesGroup


class CustomSearching(StatesGroup):
    janr = State()
    year = State()
    coast = State()
    country = State()
    box_office = State()
    rating = State()
