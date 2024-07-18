from aiogram.fsm.state import StatesGroup, State


class RandomFilmSerial(StatesGroup):
    type = State()
    criteries_yes_or_no = State()
    year = State()
    rating = State()
    age_rating = State()
    movie_length = State()
    series_length = State()
    janr = State()
    country = State()

