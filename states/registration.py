from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    login_registration = State()
    name = State()
    password = State()
    email = State()
    phone_number = State()
