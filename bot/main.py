import asyncio

from loguru import logger
from aiogram import Dispatcher, Bot
from asyncpg import Pool
from asyncpg import create_pool
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import load_config, Config
from bot.handlers import register_all_handlers
from bot.database import create_database
from bot.middleware import DBMidlleware, PaymentMidlleware
from bot.services import upload_photos

async def main():
    logger.info('Bot started...')
    config: Config = load_config()

    await create_database()

    bot: Bot = Bot(token=(config.tg_bot.token), parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    pool: Pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port
    )

    dp.middleware.setup(DBMidlleware(pool))
    dp.middleware.setup(PaymentMidlleware(config.ym.token, config.ym.account_number, config.ym.redirect_uri))

    register_all_handlers(dp)
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await bot.close()

def start_bot():
    try:
        asyncio.run(main())
    except Exception as ex:
        logger.error(ex)
