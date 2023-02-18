import os

import asyncpg
from asyncpg import Connection, Record
from loguru import logger
from aiogram.types import User

from bot.config import load_environment

ENV = load_environment()

async def create_database():
    connection: Connection = None
    try:
        connection = await asyncpg.connect(
            database=ENV('DATABASE'),
            user=ENV('USER'),
            password=ENV('PASSWORD'),
            host=ENV('HOST'),
            port=ENV('PORT')
        )
        logger.debug("Connection to PostgreSQL DB successful")

        create_db_command = open(os.path.join('bot', 'database', 'create_db.sql'), 'r', encoding='utf-8').read()
        await connection.execute(create_db_command)
        logger.debug("Tables has been created")

        await connection.close()

    except Exception as e:
        logger.error(f"The error '{e}' occurred")
    return connection

class Database:
    """Db abstraction layer"""
    ADD_NEW_USER = "INSERT INTO Users(id, username, first_name, last_name) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING RETURNING id"
    ADD_NEW_USER_REFERRAL = "INSERT INTO Users(id, username, first_name, last_name, referral) VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING RETURNING id"
    ADD_NEW_GOOD = "INSERT INTO Goods(title, price, game_id) VALUES ($1, $2, (SELECT id FROM Games WHERE name = $3))"
    ADD_MONEY = "UPDATE Users SET balance=balance+$1 WHERE id = $2"
    CHECK_BALANCE = "SELECT balance FROM Users WHERE id = $1"
    GET_GAMES = "SELECT name FROM Games"
    GET_GOODS = "SELECT id, title, price FROM Goods WHERE available = 't' AND game_id = (SELECT id FROM Games WHERE name = $1)"
    DELETE_GOOD = "UPDATE Goods SET available = 'f' WHERE id = $1"
    ADD_PROMO = "INSERT INTO Promos(name, value) VALUES ($1, $2)"
    GET_PROMO = "SELECT id, name, value FROM Promos WHERE active = 't'"
    DELETE_PROMO = "UPDATE Promos SET active = 'f' WHERE id = $1"
    CHECK_MY_REFERRALS = "SELECT COUNT(referral) FROM Users WHERE referral = $1"
    CHECK_PROMO = "SELECT EXISTS(SELECT name FROM Promos WHERE active = 't' AND name = $1)"
    USE_PROMO = "INSERT INTO Used_Promos(user_id, promo_id) VALUES ($1, (SELECT id FROM Promos WHERE active = 't' AND name = $2)) ON CONFLICT DO NOTHING RETURNING (SELECT value FROM Promos WHERE active = 't' AND name = $2)"

    def __init__(self, connection):
        self.connection: Connection = connection

    async def add_new_user(self, referral: int=None):
        user = User.get_current()
        chat_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        args = chat_id, username, first_name, last_name
        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER
        record_id = await self.connection.fetchval(command, *args)
        return record_id

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = User.get_current().id
        return await self.connection.fetchval(command, user_id)

    async def add_money(self, money: int):
        command = self.ADD_MONEY
        user_id = User.get_current().id
        return await self.connection.fetchval(command, money, user_id)

    async def get_games(self) -> list[Record]:
        command = self.GET_GAMES
        records = await self.connection.fetch(command)
        result = [record['name'] for record in records]
        return result

    async def get_goods(self, game: str) -> list[Record]:
        command = self.GET_GOODS
        records = await self.connection.fetch(command, game)
        result = [dict(record) for record in records] if records else None
        return result

    async def del_good(self, good_id: int):
        command = self.DELETE_GOOD
        return await self.connection.fetchval(command, good_id)

    async def add_good(self, title: str, price: int, good: str):
        command = self.ADD_NEW_GOOD
        return await self.connection.fetchval(command, title, price, good)

    async def add_promo(self, name: str, value: int):
        command = self.ADD_PROMO
        return await self.connection.fetchval(command, name, value)

    async def get_promo(self):
        command = self.GET_PROMO
        records = await self.connection.fetch(command)
        result = [dict(record) for record in records] if records else None
        return result

    async def del_promo(self, promo_id: int):
        command = self.DELETE_PROMO
        return await self.connection.fetchval(command, promo_id)

    async def check_referrals(self, user_id: int):
        command = self.CHECK_MY_REFERRALS
        return await self.connection.fetchval(command, user_id)

    async def check_promo(self, promo: str):
        command = self.CHECK_PROMO
        return await self.connection.fetchval(command, promo)

    async def use_promo(self, user_id: int, promo: str):
        command = self.USE_PROMO
        return await self.connection.fetchval(command, user_id, promo)
