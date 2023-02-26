from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher import FSMContext

from bot.config import load_environment
from bot.lexicon import RU_LEXICON
from bot.keyboards import admin_panel_keyboard, games_keyboard, edit_goods, goods_keyboard, cancel_button, edit_promos, promo_keyboard
from bot.database import Database
from bot.services import get_goods_description, get_promos_description, upload_photos
from bot.states import AdminState

ENV = load_environment()

async def upload_command(message: Message, db: Database):
    await db.insert_games()
    is_upload = await upload_photos(db, message)
    await message.answer(RU_LEXICON['is_upload'])
    is_insert = await db.check_goods()
    if not is_insert:
        message = await message.answer(RU_LEXICON['insert_goods_process'])
        await db.insert_goods()
        await message.edit_text(text=RU_LEXICON['insert_goods_success'])
    else:
        await message.answer(text=RU_LEXICON['insert_goods_success'])

async def admin_panel_command(message: Message):
    await message.answer(RU_LEXICON['admin_panel'], reply_markup=admin_panel_keyboard())

async def admin_panel_callback(callback: CallbackQuery, state: FSMContext):
    if state:
        await state.finish()
    await callback.message.edit_text(RU_LEXICON['admin_panel'], reply_markup=admin_panel_keyboard())
    await callback.answer()

async def choice_game_process(callback: CallbackQuery, db: Database):
    games = await db.get_games()
    await callback.message.edit_text(text=RU_LEXICON['choice_game'], reply_markup=games_keyboard(games))
    await callback.answer()

async def your_goods(callback: CallbackQuery, db: Database):
    goods = await db.get_goods(callback.data.split(':')[1])
    text = get_goods_description(goods)
    await callback.message.edit_text(text=text, reply_markup=edit_goods(callback.data.split(':')[1]))
    await callback.answer()

async def choice_good_for_delete(callback: CallbackQuery, db: Database):
    goods = await db.get_goods(callback.data.split(':')[1])
    if goods:
        await callback.message.edit_text(text=RU_LEXICON['choice_good_for_delete'], reply_markup=goods_keyboard(goods, delete=True))
        await callback.answer()
    else:
        await callback.answer(text=RU_LEXICON['no_available_goods'], show_alert=True)

async def delete_good(callback: CallbackQuery, db: Database):
    deleted_good = await db.del_good(int(callback.data.split(':')[1]))
    await admin_panel_callback(callback, state=None)
    await callback.answer(text=RU_LEXICON['success_delete'])

async def add_good_button(callback: CallbackQuery):
    await AdminState.add_good.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(game=callback.data.split(':')[1])
    await callback.message.edit_text(text=RU_LEXICON['add_good'], reply_markup=cancel_button())
    await callback.answer()

async def add_good_process(message: Message, db: Database, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    title, price = message.text.split('\n')
    new_good = await db.add_good(title, int(price), data['game'])
    await message.answer(text=RU_LEXICON['success_add_good'])

async def promo_button(callback: CallbackQuery, db: Database):
    promos = await db.get_promo()
    text = get_promos_description(promos)
    await callback.message.edit_text(text=text, reply_markup=edit_promos())

async def add_promo_button(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['add_promo'], reply_markup=cancel_button())
    await AdminState.add_promo.set()
    await callback.answer()

async def add_promo_process(message: Message, db: Database, state: FSMContext):
    await state.finish()
    name, value = message.text.split()
    '''Сделать проверку введенного промокода'''
    await db.add_promo(name, int(value))
    await message.answer(text=RU_LEXICON['success_add_promo'])

async def choice_promo_for_delete(callback: CallbackQuery, db: Database):
    promos = await db.get_promo()
    if promos:
        await callback.message.edit_text(text=RU_LEXICON['choice_promo_for_delete'], reply_markup=promo_keyboard(promos))
        await callback.answer()
    else:
        await callback.answer(text=RU_LEXICON['no_active_promo'], show_alert=True)

async def delete_promo(callback: CallbackQuery, db: Database):
    await db.del_promo(int(callback.data.split(':')[1]))
    await admin_panel_callback(callback, state=None)
    await callback.answer(text=RU_LEXICON['success_delete_promo'])

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(upload_command, IDFilter(ENV('ADMIN_ID')), commands='upload')
    dp.register_message_handler(admin_panel_command, IDFilter(ENV('ADMIN_ID')), commands='admin')
    dp.register_callback_query_handler(admin_panel_callback, text='admin', state='*')
    dp.register_callback_query_handler(choice_game_process, text='games')
    dp.register_callback_query_handler(your_goods, text_startswith='edit_game')
    dp.register_callback_query_handler(choice_good_for_delete, text_startswith='delete_good_button')
    dp.register_callback_query_handler(delete_good, text_startswith='del_good')
    dp.register_callback_query_handler(add_good_button, text_startswith='add_good')
    dp.register_message_handler(add_good_process, state=AdminState.add_good)
    dp.register_callback_query_handler(promo_button, text='promo_list')
    dp.register_callback_query_handler(add_promo_button, text='add_promo')
    dp.register_message_handler(add_promo_process, state=AdminState.add_promo)
    dp.register_callback_query_handler(choice_promo_for_delete, text='delete_promo')
    dp.register_callback_query_handler(delete_promo, text_startswith='del_promo')
