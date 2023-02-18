from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.payments.qiwi import create_invoice, check_payment
from pyqiwip2p import AioQiwiP2P
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

TOKEN = '5674599769:AAHHltnAtCOEETEnZI3x2efgpN6Kdnhbq9E'

QIWI_PRIV_KEY = "f1bf351a79eea75eb4f34ba031778816"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
p2p = AioQiwiP2P(auth_key=QIWI_PRIV_KEY)

async def create_invoice(amount: int):
    new_bill = await p2p.bill(amount=amount, lifetime=15)
    print(new_bill.bill_id, new_bill.pay_url)
    return new_bill.pay_url, new_bill.bill_id

async def check_payment(bill_id: int) -> bool:
    return await p2p.check(bill_id=bill_id).status


def keyboard_payment(url: str, bill_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Ссылка на оплату', url=url),
        InlineKeyboardButton(text='Проверить платеж', callback_data=f"check:{bill_id}")
    ]
    keyboard.insert(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])  # обработчик событий message
async def cmd_start(message: Message) -> None:
    pay_link, bill_id = await create_invoice(5)
    await message.answer(text='Ваш счет на оплату 5 руб: ', reply_markup=keyboard_payment(pay_link, bill_id))

@dp.callback_query_handler(text_startswith='check')
async def check_payment_button(callback: CallbackQuery):
    bill_id = int(callback.data.split(':')[1])
    is_paid = check_payment(bill_id)
    if is_paid:
        await callback.message.answer('Ваш счет оплачен')
    else:
        await callback.message.answer('Вы не оплатили счет')

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
