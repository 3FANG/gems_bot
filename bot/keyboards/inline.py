from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Brawl Stars', callback_data='pay_game:Brawl Stars'),
        InlineKeyboardButton(text='Другие игры', callback_data='another_games'),
        InlineKeyboardButton(text='Мои заказы', callback_data='my_orders:1'),
        InlineKeyboardButton(text='Баланс', callback_data='balance'),
        InlineKeyboardButton(text='Бесплатные гемы', callback_data='free_gems')
    ]
    keyboard.add(*buttons)
    return keyboard

def free_gems_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Промокоды', callback_data='promo'),
        InlineKeyboardButton(text='Реферальная программа', callback_data='referral_program'),
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
        InlineKeyboardButton(text='⚪️ Промокоды', callback_data='promo_list')
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
                InlineKeyboardButton(text=good['title'], callback_data=f"good:{good['id']}")
            )
        keyboard.add(
            InlineKeyboardButton(text='◀ Назад', callback_data='start_button')
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
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Редактировать ссылку', callback_data='edit_link'),
        InlineKeyboardButton(text='◀ Назад', callback_data='free_gems')
    ]
    keyboard.add(*buttons)
    return keyboard

def cancel_edit_link(back=False) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='❌ Отмена' if not back else '◀ Назад', callback_data='referral_program')
    ]])
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

def cancel_buy_good_button() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_order'),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_code_button(order_id: int|str, user_id: str|int) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='⏳ Запросить код', callback_data=f"get_code:{order_id}:{user_id}")
    ]
    keyboard.add(*buttons)
    return keyboard

def success_donate_keyboard(order_id: int|str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='⚠️ Неверный код', callback_data=f"invalid_code:{order_id}"),
        InlineKeyboardButton(text='✅ Донат прошел успешно', callback_data=f"success_donate:{order_id}")
    ]
    keyboard.add(*buttons)
    return keyboard

def pagination_orders_keyboard(orders: list[dict], page: int, pages_count: int) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for order in orders[(page-1)*10:page*10]:
        status = None
        if order['status'] == 'wait':
            status = '🕓'
        elif order['status'] == 'check':
            status = '🔑'
        elif order['status'] == 'send_code':
            status = '✉️'
        elif order['status'] == 'false_code':
            status = '❗️'
        elif order['status'] == 'change_code':
            status = '🔄'
        else:
            status = '✅'
        text = f"{status} | {order['title']} | {order['price']}₽"
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=f"order_details:{order['id']}")
        )
    keyboard.row(
        InlineKeyboardButton(text='<', callback_data='pagination_backward'),
        InlineKeyboardButton(text=f"{page}/{pages_count}", callback_data='none'),
        InlineKeyboardButton(text='>', callback_data='pagination_forward')
    )
    keyboard.add(
        InlineKeyboardButton(text='◀ Назад', callback_data='start_button')
    )
    return keyboard

def order_details_keyboard(order_id: int|str, page: int|str, raw_status: str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='✏️ Изменить почту', callback_data=f"change_mail:{order_id}"),
        InlineKeyboardButton(text='◀ Назад', callback_data=f"my_orders:{page}")
    ]
    if raw_status == 'send_code':
        buttons.insert(
            1,
            InlineKeyboardButton(text='📤 Отправить код', callback_data=f"send_code:{order_id}")
        )
    elif raw_status == 'false_code':
        buttons.insert(
            1,
        InlineKeyboardButton(text='✏️ Изменить код', callback_data=f"change_code:{order_id}")
        )
    buttons = buttons if raw_status != 'success' else [buttons[-1]]
    keyboard.add(*buttons)
    return keyboard

def sending_code_button(order_id: int) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='📤 Отправить код', callback_data=f"send_code:{order_id}")
    ]])
    return keyboard

def cancel_edit_order(order_id: int|str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='❌ Отмена', callback_data=f"order_details:{order_id}"),
    ]
    keyboard.add(*buttons)
    return keyboard
