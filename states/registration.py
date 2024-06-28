from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    email = State()
    phone_number = State()
