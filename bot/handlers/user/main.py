from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.keyboards import main_keyboard, free_gems_keyboard, another_games_keyboard, promo_back_button, goods_keyboard, edit_referral_keyboard, top_up_balance, cancel_top_up_balance, invoice_buttons
from bot.lexicon import RU_LEXICON
from bot.database import Database
from bot.services import get_link, check_valid_input
from bot.states import UserState
from bot.payments import create_invoice, check_invoice

async def start_command(message: Message, db: Database, state: FSMContext):
    await state.finish()
    referral = message.get_args()
    await db.add_new_user(referral=int(referral) if referral else None)
    await message.answer_photo(photo='AgACAgIAAxkBAAIBBmPo95_-1i7A5ZN2aPAQvnmjtD-4AAKpyTEbFk1IS8mPs0HTdjStAQADAgADeAADLgQ',
        caption=RU_LEXICON['start'],
        reply_markup=main_keyboard())

async def start_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAIBBmPo95_-1i7A5ZN2aPAQvnmjtD-4AAKpyTEbFk1IS8mPs0HTdjStAQADAgADeAADLgQ',
        caption=RU_LEXICON['start'],
        reply_markup=main_keyboard())
    await callback.answer()

async def free_gems_button(callback: CallbackQuery, db: Database):
    balance = await db.check_balance()
    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['free_gems'].format(balance),
        reply_markup=free_gems_keyboard())
    await callback.answer()

async def promo_button(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['promo'], reply_markup=promo_back_button())
    await callback.answer()

async def promo_command(message: Message, db: Database):
    promo = message.get_args()
    promo_enable = await db.check_promo(promo)
    if promo_enable:
        value = await db.use_promo(int(message.from_user.id), promo)
        if value:
            await message.answer(text=RU_LEXICON['success_promo'].format(value))
            await db.add_money(value)
        else:
            await message.answer(text=RU_LEXICON['no_no_no'])
    else:
        await message.answer(text=RU_LEXICON['no_promo'])

async def my_orders_button(callback: CallbackQuery):
    '''Смотреть в БД заказы юзера'''
    await callback.answer(text=RU_LEXICON['no_orders']) #если нет заказов
    await callback.answer()

async def another_games_buttons(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['games_list'], reply_markup=another_games_keyboard())
    await callback.answer()

async def game_button(callback: CallbackQuery, db: Database):
    goods = await db.get_goods(callback.data.split(':')[1])
    await callback.message.answer(text=RU_LEXICON['goods_list'], reply_markup=goods_keyboard(goods)) #edit_photo
    await callback.answer()

async def referral_program_button(callback: CallbackQuery, db: Database):
    user_id = callback.message.from_user.id
    botinfo = await callback.bot.get_me()
    link = get_link(user_id, botinfo)
    count_referrals = await db.check_referrals(user_id)
    await callback.message.edit_text(text=RU_LEXICON['referral_link'].format(link, count_referrals), reply_markup=edit_referral_keyboard())  #исправить
    await callback.answer()

async def balance_button(callback: CallbackQuery, db: Database, state: FSMContext):
    await state.finish()
    balance = await db.check_balance()
    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['balance'].format(balance), reply_markup=top_up_balance())
    await callback.answer()

async def top_up_balance_button(callback: CallbackQuery):
    await UserState.add_money.set()
    await callback.message.edit_text(text=RU_LEXICON['value_add'], reply_markup=cancel_top_up_balance())
    await callback.answer()

async def create_invoice_process(message: Message, yoomoney_account_number: str, state: FSMContext):
    message_text = message.text
    amount = check_valid_input(message_text)
    if amount:
        await state.finish()
        wait_message = await message.answer('Подождите, создается счет на оплату...')
        invoice_link, lable = await create_invoice(yoomoney_account_number, amount)
        await wait_message.edit_text(text=RU_LEXICON['add_money_details'].format(amount, invoice_link, lable), reply_markup=invoice_buttons(invoice_link, lable, amount))
    else:
        await message.answer(text=RU_LEXICON['invalid_input'], reply_markup=cancel_top_up_balance())

async def check_payed_button(callback: CallbackQuery, yoomoney_token: str, db: Database):
    lable = callback.data.split(':')[1]
    amount = callback.data.split(':')[2]
    is_payed = await check_invoice(lable, yoomoney_token)
    if is_payed:
        await db.add_money(int(amount))
        await callback.answer(text='✅ Баланс успешно пополнен', show_alert=True)
        await start_callback(callback)
    else:
        await callback.answer(text='Платеж не найден!', show_alert=True)

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start', state='*')
    dp.register_callback_query_handler(start_callback, text='start_button')
    dp.register_callback_query_handler(free_gems_button, text='free_gems')
    dp.register_callback_query_handler(promo_button, text='promo')
    dp.register_message_handler(promo_command, commands='promo')
    dp.register_callback_query_handler(my_orders_button, text='my_orders')
    dp.register_callback_query_handler(another_games_buttons, text='another_games')
    dp.register_callback_query_handler(game_button, text_startswith='pay_game')
    dp.register_callback_query_handler(referral_program_button, text='referal_program')
    dp.register_callback_query_handler(balance_button, text='balance', state='*')
    dp.register_callback_query_handler(top_up_balance_button, text='top_up_balance')
    dp.register_message_handler(create_invoice_process, state=UserState.add_money)
    dp.register_callback_query_handler(check_payed_button, text_startswith='check_payed')
