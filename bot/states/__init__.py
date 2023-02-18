from aiogram.dispatcher.filters.state import StatesGroup, State

class AdminState(StatesGroup):
    add_good = State()
    add_promo = State()

class UserState(StatesGroup):
    add_money = State()
