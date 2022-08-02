from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    weather = State()
    chat = State()
    compose = State()
    cancel = State()
