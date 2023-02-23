from aiogram.dispatcher.filters.state import StatesGroup, State

class AdminState(StatesGroup):
    add_good = State()
    add_promo = State()

class UserState(StatesGroup):
    add_money = State()
    send_mail = State()
    send_code = State()
    pagination = State()
    edit_mail = State()
    edit_code = State()
    edit_link = State()
