from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Brawl Stars', callback_data='pay_game:Brawl Stars'),
        InlineKeyboardButton(text='Другие игры', callback_data='another_games'),
        InlineKeyboardButton(text='Мои заказы', callback_data='my_orders'),
        InlineKeyboardButton(text='Баланс', callback_data='balance'),
        InlineKeyboardButton(text='Бесплатные гемы', callback_data='free_gems')
    ]
    keyboard.add(*buttons)
    return keyboard

def free_gems_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Промокоды', callback_data='promo'),
        InlineKeyboardButton(text='Реферальная программа', callback_data='referal_program'),
        InlineKeyboardButton(text='◀ Назад', callback_data='start_button')
    ]
    keyboard.add(*buttons)
    return keyboard

def another_games_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    games = ['Clash of Clans', 'Clash Royale']
    for game in games:
        keyboard.insert(
            InlineKeyboardButton(text=game, callback_data=f"pay_game:{game}")
        )
    keyboard.add(InlineKeyboardButton(text='◀ Назад', callback_data='start_button'))
    return keyboard

def promo_back_button() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='◀ Назад', callback_data='free_gems')
    )
    return keyboard

def admin_panel_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='⚪️ Товары', callback_data='games'),
        InlineKeyboardButton(text='⚪️ Поромокоды', callback_data='promo_list')
    ]
    keyboard.add(*buttons)
    return keyboard

def games_keyboard(games: list[str]) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for game in games:
        keyboard.add(
            InlineKeyboardButton(text=game, callback_data=f"edit_game:{game}")
        )
    keyboard.add(
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
    )
    return keyboard

def goods_keyboard(goods: list[dict], delete=False) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    if delete:
        for good in goods:
            keyboard.insert(
                InlineKeyboardButton(text=f"🗑 {good['title']}", callback_data=f"del_good:{good['id']}")
            )
        keyboard.add(
            InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
        )
    else:
        for good in goods:
            keyboard.insert(
                InlineKeyboardButton(text=good['title'], callback_data=f"good:{good['title']}")
            )
    return keyboard

def edit_goods(game: str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='🗑 Удалить товар', callback_data=f"delete_good_button:{game}"),
        InlineKeyboardButton(text='✅ Добавить товар', callback_data=f"add_good:{game}"),
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
    ]
    keyboard.add(*buttons)
    return keyboard

def edit_promos() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='🗑 Удалить промокод', callback_data=f"delete_promo"),
        InlineKeyboardButton(text='✅ Добавить промокод', callback_data=f"add_promo"),
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
    ]
    keyboard.add(*buttons)
    return keyboard

def cancel_button() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
    )
    return keyboard

def promo_keyboard(promos: list[dir]) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    for promo in promos:
        keyboard.insert(
            InlineKeyboardButton(text=f"🗑 {promo['name']}", callback_data=f"del_promo:{promo['id']}")
        )
    keyboard.add(
        InlineKeyboardButton(text='❌ Отмена', callback_data='admin')
    )
    return keyboard

def edit_referral_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        # Добавить редактирование ссылки
        InlineKeyboardButton(text='◀ Назад', callback_data='free_gems')
    ]
    keyboard.add(*buttons)
    return keyboard

def top_up_balance() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up_balance'),
        InlineKeyboardButton(text='◀ Назад', callback_data='start_button')
    ]
    keyboard.add(*buttons)
    return keyboard

def cancel_top_up_balance() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='❌ Отмена', callback_data='balance'),
    ]
    keyboard.add(*buttons)
    return keyboard

def invoice_buttons(invoice_link: str, lable: str, amount: int) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='Ссылка на оплату', url=invoice_link),
        InlineKeyboardButton(text='Проверить оплату', callback_data=f"check_payed:{lable}:{amount}")
    ]
    keyboard.add(*buttons)
    return keyboard
