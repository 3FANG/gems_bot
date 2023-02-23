import datetime
from math import ceil

from aiogram.types import User
from aiogram.types.input_media import InputMediaPhoto
from tzlocal import get_localzone

from bot.lexicon import RU_LEXICON

def get_goods_description(goods: list[dict] | None) -> str:
    text = RU_LEXICON['your_goods']
    count = 1
    if goods:
        text += '\n\n'
        for good in goods:
            text += f"{count}. Название: {good['title']} | Цена: {good['price']}₽\n"
            count += 1
    return text

def get_promos_description(promos: list[dict] | None) -> str:
    text = RU_LEXICON['your_promos']
    count = 1
    if promos:
        text += '\n\n'
        for promo in promos:
            text += f"{count}. Название: {promo['name']} | Цена: {promo['value']}₽\n"
            count += 1
    return text

def get_link(user_id: str|int, botinfo: User) -> str:
    url = 'https://t.me/'
    link = f"{url}{botinfo.username}?start={user_id if user_id.isdigit() else 'ref_' + user_id}"
    return link

def check_valid_link(link: str) -> bool:
    invalid_symbols = " !@#$%^&?*()+=~`\\/.<>,|[]\{\}"
    if len(link) > 30:
        return False
    if any(map(lambda x: x in invalid_symbols, link)):
        return False
    return True

def check_valid_input(amount: int | str) -> bool:
    try:

        return int(amount)
    except ValueError:
        return False

async def get_input_photo(photo_id: str, caption: str) -> InputMediaPhoto:
    return InputMediaPhoto(media=photo_id, caption=caption)

def check_valid_mail(mail: str) -> bool:
    try:
        if ' ' in mail:
            return False
        is_doth_after_at = mail.split('@')[1].count('.')
        if is_doth_after_at != 1:
            return False

        return True
    except:
        return False

def date_formatting(raw_date: datetime.datetime) -> str:
    timezone = get_localzone()
    timezone_into_hours = timezone.utcoffset(datetime.datetime.now())
    date = (raw_date + timezone_into_hours).strftime("%H:%M %d.%m.%Y")
    return date

def check_valid_code(code: str) -> bool:
    if len(code) != 6 or not code.isdigit() or ' ' in code:
        return False
    return int(code)

def get_pages_amount(orders_count: int) -> int:
    return ceil(orders_count/10)

def status_formatting(raw_status: str) -> str:
    if raw_status == 'wait':
        status = "📮 Ожидает ввода почты администратором"
    elif raw_status == 'send_code':
        status = "📨 Ожидает код подтверждения"
    elif raw_status == 'check':
        status = "🔑 Вход в аккаунт"
    elif raw_status == 'false_code':
        status = "❗️ Неверный код"
    elif raw_status == 'change_code':
        status = "🔄 Изменение кода"
    else:
        status = "✅ Выполнен"
    return status
