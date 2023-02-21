import time

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.keyboards import main_keyboard, free_gems_keyboard, another_games_keyboard, promo_back_button, goods_keyboard, edit_referral_keyboard, top_up_balance, cancel_top_up_balance, invoice_buttons, cancel_buy_good_button, get_code_button, success_donate_button, pagination_orders_keyboard, order_details_keyboard, cancel_edit_order
from bot.lexicon import RU_LEXICON
from bot.database import Database
from bot.services import get_link, check_valid_input, get_input_photo, check_valid_mail, date_formatting, check_valid_code, get_pages_amount, status_formatting
from bot.payments import create_invoice, check_invoice
from bot.states import UserState
from bot.config import load_environment

ENV = load_environment()

async def start_command(message: Message, db: Database):
    referral = message.get_args()
    await db.add_new_user(referral=int(referral) if referral else None)
    photo = await db.get_photo()
    if not photo:
        await message.answer(text=RU_LEXICON['no_photo'])
        return
    await message.answer_photo(photo=photo,
        caption=RU_LEXICON['start'],
        reply_markup=main_keyboard())

async def start_callback(callback: CallbackQuery, db: Database, state: FSMContext):
    if state:
        await state.finish()
    await callback.message.delete()
    photo = await db.get_photo()
    await callback.message.answer_photo(photo=photo,
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

async def my_orders_button(callback: CallbackQuery, db: Database):
    orders = await db.get_orders()
    if not orders:
        await callback.answer(text=RU_LEXICON['no_orders']) #если нет заказов
    else:
        await UserState.pagination.set()
        state = Dispatcher.get_current().current_state()
        page = int(callback.data.split(':')[1])
        await state.update_data(orders=orders, page=page, pages_amount=get_pages_amount(len(orders)))
        await callback.message.delete()
        await callback.message.answer(text=RU_LEXICON['orders_count'].format(len(orders)), reply_markup=pagination_orders_keyboard(orders, page, get_pages_amount(len(orders))))

async def process_forward_button(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] + 1 <= data['pages_amount']:
        await state.update_data(page=data['page']+1)
        await callback.message.edit_reply_markup(reply_markup=pagination_orders_keyboard(orders=data['orders'], page=data['page'] + 1, pages_count=get_pages_amount(len(data['orders']))))
    else:
        await state.update_data(page=1)
        await callback.message.edit_reply_markup(reply_markup=pagination_orders_keyboard(orders=data['orders'], page=1, pages_count=get_pages_amount(len(data['orders']))))
    await callback.answer()

async def process_backward_button(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['page'] - 1 > 0:
        await state.update_data(page=data['page']-1)
        await callback.message.edit_reply_markup(reply_markup=pagination_orders_keyboard(orders=data['orders'], page=data['page'] - 1, pages_count=get_pages_amount(len(data['orders']))))
    else:
        await state.update_data(page=data['pages_amount'])
        await callback.message.edit_reply_markup(reply_markup=pagination_orders_keyboard(orders=data['orders'], page=get_pages_amount(len(data['orders'])), pages_count=get_pages_amount(len(data['orders']))))
    await callback.answer()

async def order_button(callback: CallbackQuery, db: Database, state: FSMContext):
    await UserState.pagination.set()
    data = await state.get_data()
    page = data['page']
    order_id = int(callback.data.split(':')[1])
    await state.update_data(last_order=order_id)
    details_dict = await db.get_order_details(order_id)
    raw_date, title, price, mail, code, raw_status = details_dict.values()
    date = date_formatting(raw_date)
    status = status_formatting(raw_status)
    await callback.message.edit_text(text=RU_LEXICON['order_details'].format(date, title, price, mail, code, status), reply_markup=order_details_keyboard(order_id, page, raw_status))

async def change_mail_button(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split(':')[1]
    await UserState.edit_mail.set()
    await callback.message.edit_text(text=RU_LEXICON['edit_mail'], reply_markup=cancel_edit_order(order_id))

async def change_mail_process(message: Message, db: Database, state: FSMContext):
    data = await state.get_data()
    order_id = data['last_order']
    is_valid = check_valid_mail(message.text)
    if not is_valid:
        await message.answer(RU_LEXICON['invalid_mail'], reply_markup=cancel_edit_order(order_id))
    else:
        await UserState.pagination.set()
        raw_date, title, price, mail, code, raw_status = await db.update_mail(order_id, message.text)
        page = data['page']
        date = date_formatting(raw_date)
        status = status_formatting(raw_status)
        await message.answer(text=RU_LEXICON['order_details'].format(date, title, price, mail, code, status), reply_markup=order_details_keyboard(order_id, page, raw_status))
        '''Cообщение админу'''

async def change_code_button(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split(':')[1]
    await UserState.edit_code.set()
    await callback.message.edit_text(text=RU_LEXICON['edit_code'], reply_markup=cancel_edit_order(order_id))

async def change_code_process(message: Message, db: Database, state: FSMContext):
    data = await state.get_data()
    order_id = data['last_order']
    code = check_valid_code(message.text)
    if not code:
        await message.answer(RU_LEXICON['invalid_code'], reply_markup=cancel_edit_order(order_id))
    else:
        await UserState.pagination.set()
        raw_date, title, price, mail, code, raw_status = await db.update_code(order_id, code)
        page = data['page']
        date = date_formatting(raw_date)
        status = status_formatting(raw_status)
        await message.answer(text=RU_LEXICON['order_details'].format(date, title, price, mail, code, status), reply_markup=order_details_keyboard(order_id, page, raw_status))
        '''Сообщение админу'''

async def another_games_buttons(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['games_list'], reply_markup=another_games_keyboard())
    await callback.answer()

async def game_button(callback: CallbackQuery, db: Database):
    game = callback.data.split(':')[1]
    goods = await db.get_goods(game)
    if goods:
        photo_id = await db.get_photo(game)
        await callback.message.delete()
        await callback.message.answer_photo(photo=photo_id, caption=RU_LEXICON['goods_list'], reply_markup=goods_keyboard(goods))
        await callback.answer()
    else:
        await callback.answer(text=RU_LEXICON['no_goods'], show_alert=True)

async def buy_good_button(callback: CallbackQuery, db: Database):
    good_id = int(callback.data.split(':')[1])
    name, price = await db.get_good_details(good_id)
    user_balance = await db.check_balance()
    if user_balance < price:
        await callback.answer(RU_LEXICON['no_money'])
    else:
        photo_id = callback.message.photo[-1].file_id
        photo = await get_input_photo(photo_id=photo_id, caption=RU_LEXICON['good_details'].format(name, price))
        await UserState.send_mail.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(good=name, price=price, good_id=good_id)
        await callback.message.edit_media(media=photo, reply_markup=cancel_buy_good_button())
        await callback.answer()

async def send_mail_process(message: Message, db: Database, state: FSMContext):
    is_valid = check_valid_mail(message.text)
    if not is_valid:
        await message.reply(RU_LEXICON['invalid_mail'], reply_markup=cancel_buy_good_button())
    else:
        data = await state.get_data()
        await db.spend_money(data['price'])
        mail = message.text
        good_id = data['good_id']
        order_id, raw_date, client_username = await db.add_order(good_id, mail)
        date = date_formatting(raw_date)
        await message.answer(RU_LEXICON['order_create'])
        good = data['good']
        price = data['price']
        await message.bot.send_message(chat_id=ENV("ADMIN_ID"), text=RU_LEXICON['create_order_push'].format(date, order_id, '@' + client_username if not client_username.isdigit() else client_username, mail, good, price), reply_markup=get_code_button(order_id, message.from_user.id))
        await state.finish()

async def send_code_process(callback: CallbackQuery):
    order_id, client_id = [int(data) for data in callback.data.split(':')[1:]]
    await UserState.send_code.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(order_id=order_id)
    await callback.bot.send_message(chat_id=client_id, text=RU_LEXICON['get_code'])
    await callback.message.edit_reply_markup()
    await callback.answer(RU_LEXICON['notification_was_sended'])

async def check_code_process(message: Message, db: Database, state: FSMContext):
    code = check_valid_code(message.text)
    if not code:
        await message.answer(RU_LEXICON['invalid_code'])
    else:
        data = await state.get_data()
        order_id = data['order_id']
        await message.answer(RU_LEXICON['valid_code'])
        await state.finish()
        await db.update_order_code(order_id, code)
        client_username, mail, good, price = await db.get_order_notification(order_id)
        await message.bot.send_message(chat_id=ENV("ADMIN_ID"), text=RU_LEXICON['send_code_push'].format(order_id, '@' + client_username if not client_username.isdigit() else client_username, mail, code, good, price), reply_markup=success_donate_button(order_id))
        await state.finish()

async def success_donate_button(callback: CallbackQuery):
    pass

async def cancel_order_button(callback: CallbackQuery, db: Database, state: FSMContext):
    await state.finish()
    await callback.answer(RU_LEXICON['cancel_order'])
    await start_callback(callback, db, state=None)

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
    lable, amount = callback.data.split(':')[1:]
    is_payed = await check_invoice(lable, yoomoney_token)
    if is_payed:
        await db.add_money(int(amount))
        await callback.answer(text=RU_LEXICON['success_balance'], show_alert=True)
        await start_callback(callback, db, state=None)
    else:
        await callback.answer(text='Платеж не найден!', show_alert=True)

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(start_command, commands='start', state=UserState.pagination)
    dp.register_callback_query_handler(start_callback, text='start_button', state='*')
    dp.register_callback_query_handler(free_gems_button, text='free_gems')
    dp.register_callback_query_handler(promo_button, text='promo')
    dp.register_message_handler(promo_command, commands='promo')
    dp.register_callback_query_handler(my_orders_button, text_startswith='my_orders')
    dp.register_callback_query_handler(my_orders_button, text_startswith='my_orders', state=UserState.pagination)
    dp.register_callback_query_handler(another_games_buttons, text='another_games')
    dp.register_callback_query_handler(game_button, text_startswith='pay_game')
    dp.register_callback_query_handler(referral_program_button, text='referal_program')
    dp.register_callback_query_handler(balance_button, text='balance', state='*')
    dp.register_callback_query_handler(top_up_balance_button, text='top_up_balance')
    dp.register_message_handler(create_invoice_process, state=UserState.add_money)
    dp.register_callback_query_handler(check_payed_button, text_startswith='check_payed')
    dp.register_callback_query_handler(buy_good_button, text_startswith='good')
    dp.register_message_handler(send_mail_process, state=UserState.send_mail)
    dp.register_callback_query_handler(cancel_order_button, text='cancel_order', state='*')
    dp.register_callback_query_handler(send_code_process, text_startswith='get_code')
    dp.register_message_handler(check_code_process, state=UserState.send_code)
    dp.register_callback_query_handler(order_button, text_startswith='order_details', state='*')
    dp.register_callback_query_handler(change_mail_button, text_startswith='change_mail', state=UserState.pagination)
    dp.register_message_handler(change_mail_process, state=UserState.edit_mail)
    dp.register_callback_query_handler(change_code_button, text_startswith='change_code', state=UserState.pagination)
    dp.register_message_handler(change_code_process, state=UserState.edit_code)
    dp.register_callback_query_handler(process_backward_button, text='pagination_backward', state=UserState.pagination)
    dp.register_callback_query_handler(process_forward_button, text='pagination_forward', state=UserState.pagination)
