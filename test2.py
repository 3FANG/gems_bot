import random
import string

from bot.config import load_environment
from yoomoney import Authorize, Client, Quickpay

from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.payments.qiwi import create_invoice, check_payment
from pyqiwip2p import AioQiwiP2P
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

TOKEN = '5674599769:AAHHltnAtCOEETEnZI3x2efgpN6Kdnhbq9E'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
ENV = load_environment()

def check_availability_token():
    return bool(ENV('YOOMONEY_TOKEN'))

def get_token():
    Authorize(
        client_id=ENV("CLIENT_ID"),
        redirect_uri=ENV("REDIRECT_URI"),
        scope=["account-info",
                "operation-history",
                "operation-details",
                "incoming-transfers",
                "payment-p2p",
                "payment-shop",
                ]
        )

def create_invoice(amount: int) -> str:
    letters_and_digits = string.ascii_lowercase + string.digits
    label = ''.join(random.sample(letters_and_digits, 10))
    quickpay = Quickpay(
            receiver=ENV("YOOMONEY_ACCOUNT_NUMBER"),
            quickpay_form="shop",
            targets="Replenishment of the balance",
            paymentType="SB",
            sum=amount,
            label=label
            )
    return quickpay.redirected_url, label

def check_invoice(label: str):
    client = Client(ENV('YOOMONEY_TOKEN'))
    history = client.operation_history(label=label)
    print(history.operations)

def yoomoney_token():
    is_token = check_availability_token()
    if not is_token:
        get_token()

def keyboard_payment(url: str, lable: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Ссылка на оплату', url=url),
        InlineKeyboardButton(text='Проверить платеж', callback_data=f"check:{lable}")
    ]
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])  # обработчик событий message
async def cmd_start(message: Message) -> None:
    pay_link, label = create_invoice(5)
    await message.answer(text='Ваш счет на оплату 5 руб: ', reply_markup=keyboard_payment(pay_link, label))

@dp.callback_query_handler(text_startswith='check')
async def check_payment_button(callback: CallbackQuery):
    check_invoice(callback.data.split(':')[1])

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)
