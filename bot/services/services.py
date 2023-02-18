from aiogram.types import User

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

def get_link(user_id: str | int, botinfo: User) -> str:
    url = 'https://t.me/'
    link = f"{url}{botinfo.username}?start={user_id}"
    return link

def check_valid_input(amount: int | str) -> bool:
    try:
        return int(amount)
    except ValueError:
        return False
