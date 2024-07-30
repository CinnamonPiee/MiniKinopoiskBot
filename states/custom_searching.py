from aiogram.fsm.state import State, StatesGroup


class CustomSearching(StatesGroup):
    type_choice = State()
    count = State()
    janr = State()
    year = State()
    rating = State()
    age_rating = State()
    country = State()
    movie_length = State()
    series_length = State()
