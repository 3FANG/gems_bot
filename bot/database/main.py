import os
import datetime

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
<<<<<<< HEAD
    ADD_NEW_GOOD = "INSERT INTO Goods(title, price, game_id) VALUES($1, $2, (SELECT id FROM Games WHERE name = $3))"
=======
    ADD_NEW_USER_REFERRAL_OWN_LINK = "INSERT INTO Users(id, username, first_name, last_name, referral) VALUES ($1, $2, $3, $4, (SELECT id FROM Users WHERE ref_link = $5)) ON CONFLICT DO NOTHING RETURNING id"
    ADD_NEW_GOOD = "INSERT INTO Goods(title, price, game_id) VALUES ($1, $2, (SELECT id FROM Games WHERE name = $3))"
>>>>>>> 58dffac861a8537299080b7ff803537d3c9d01bf
    ADD_MONEY = "UPDATE Users SET balance=balance+$1 WHERE id = $2"
    CHECK_BALANCE = "SELECT balance FROM Users WHERE id = $1"
    GET_GAMES = "SELECT name FROM Games"
    GET_GOODS = "SELECT id, title, price FROM Goods WHERE available = 't' AND game_id = (SELECT id FROM Games WHERE name = $1)"
    GET_GOOD = "SELECT title, price FROM Goods WHERE id = $1"
    DELETE_GOOD = "UPDATE Goods SET available = 'f' WHERE id = $1"
    ADD_PROMO = "INSERT INTO Promos(name, value) VALUES ($1, $2)"
    GET_PROMO = "SELECT id, name, value FROM Promos WHERE active = 't'"
    DELETE_PROMO = "UPDATE Promos SET active = 'f' WHERE id = $1"
    CHECK_MY_REFERRALS = "SELECT COUNT(referral) FROM Users WHERE referral = $1"
    CHECK_PROMO = "SELECT EXISTS(SELECT name FROM Promos WHERE active = 't' AND name = $1)"
    USE_PROMO = "INSERT INTO Used_Promos(user_id, promo_id) VALUES ($1, (SELECT id FROM Promos WHERE active = 't' AND name = $2)) ON CONFLICT DO NOTHING RETURNING (SELECT value FROM Promos WHERE active = 't' AND name = $2)"
    CHECK_PHOTO = "SELECT EXISTS(SELECT * FROM Photos)"
    ADD_PHOTO = "INSERT INTO Photos(photo_id, photo_unique_id, file_path, game_id) VALUES($1, $2, $3, (SELECT id FROM Games WHERE name = $4))"
    GET_MAIN_PHOTO = "SELECT photo_id FROM Photos WHERE game_id is null"
    GET_PHOTO = "SELECT photo_id FROM Photos WHERE game_id = (SELECT id FROM Games WHERE name = $1)"
    SPEND_MONEY = "UPDATE Users SET balance = balance - $1 WHERE id = $2"
    ADD_ORDER = "INSERT INTO Orders(user_id, good_id, mail) VALUES($1, $2, $3) RETURNING id, registed, (SELECT COALESCE(username, id::VARCHAR(30)) FROM Users WHERE id = $1)"
    GET_ORDER_NOTIFICATION = "SELECT COALESCE(username, Users.id::VARCHAR(30)), mail, Goods.title, Goods.price FROM Orders JOIN Users ON Users.id = Orders.user_id JOIN Goods ON Goods.id = Orders.good_id WHERE Orders.id = $1"
    UPDATE_ORDER_CODE = "UPDATE Orders SET code = $2, status = 'check' WHERE id = $1"
    GET_ORDERS = "SELECT registed, title, price, mail, code, status, Orders.id FROM Orders JOIN Goods ON Goods.id = Orders.good_id WHERE user_id = $1"
    GET_ORDER = "SELECT registed, title, price, mail, code, status FROM Orders JOIN Goods ON Goods.id = Orders.good_id WHERE Orders.id = $1"
    UPDATE_MAIL = "UPDATE Orders SET mail = $2 WHERE id = $1"
    UPDATE_CODE = "UPDATE Orders SET code = $2, status = 'change_code' WHERE id = $1"
    GET_ORDER_DATE = "SELECT registed FROM Orders WHERE id = $1"
    UPDATE_STATUS = "UPDATE Orders SET status = $2 WHERE id = $1 RETURNING user_id, registed"
<<<<<<< HEAD
    INSERT_GAMES = "INSERT INTO Games(name) VALUES($1)"
    CHECK_GAMES = "SELECT EXISTS(SELECT * FROM Games)"
    CHECK_GOODS = "SELECT EXISTS(SELECT * FROM Goods)"
=======
    CHECK_LINK_EXISTS = "SELECT EXISTS(SELECT ref_link FROM Users WHERE ref_link = $1)"
    UPDATE_REFLINK = "UPDATE Users SET ref_link = $2 WHERE id = $1"
    GET_LINK = "SELECT CASE WHEN ref_link is not null THEN ref_link ELSE id::VARCHAR(30) END FROM Users WHERE id = $1"
>>>>>>> 58dffac861a8537299080b7ff803537d3c9d01bf

    def __init__(self, connection):
        self.connection: Connection = connection

    async def add_new_user(self, referral: int|str=None):
        user = User.get_current()
        chat_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        args = chat_id, username, first_name, last_name
        if referral:
            if referral.isdigit():
                args += (int(referral),)
                command = self.ADD_NEW_USER_REFERRAL
            else:
                args += (referral.split('_')[1],)
                command = self.ADD_NEW_USER_REFERRAL_OWN_LINK
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

    async def get_good_details(self, good_id: int) -> list[str]:
        command = self.GET_GOOD
        return await self.connection.fetchrow(command, good_id)

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

    async def check_photo(self):
        command = self.CHECK_PHOTO
        return await self.connection.fetchval(command)

    async def add_photo(self, photo_id: str, photo_unique_id: str, file_path: str, game: str):
        command = self.ADD_PHOTO
        return await self.connection.fetchval(command, photo_id, photo_unique_id, file_path, game)

    async def get_photo(self, game: str=None):
        if game:
            command = self.GET_PHOTO
            return await self.connection.fetchval(command, game)
        else:
            command = self.GET_MAIN_PHOTO
            return await self.connection.fetchval(command)

    async def spend_money(self, value: int):
        command = self.SPEND_MONEY
        user_id = User.get_current().id
        return await self.connection.fetchval(command, value, user_id)

    async def add_order(self, good_id: int, mail: str) -> list[int|str]:
        command = self.ADD_ORDER
        user_id = User.get_current().id
        return await self.connection.fetchrow(command, user_id, good_id, mail)

    async def get_order_notification(self, order_id: int) -> list[int|str]:
        command = self.GET_ORDER_NOTIFICATION
        return await self.connection.fetchrow(command, order_id)

    async def update_order_code(self, order_id: int, code: int):
        command = self.UPDATE_ORDER_CODE
        return await self.connection.fetchval(command, order_id, code)

    async def get_orders(self) -> list[dict]:
        command = self.GET_ORDERS
        user_id = User.get_current().id
        records =  await self.connection.fetch(command, user_id)
        result = [dict(record) for record in records] if records else None
        return result

    async def get_order_details(self, order_id: int) -> dict:
        command = self.GET_ORDER
        row = await self.connection.fetchrow(command, order_id)
        return dict(row)

    async def update_mail(self, order_id: int, mail: str) -> list[int|str]:
        update_command = self.UPDATE_MAIL
        await self.connection.fetchval(update_command, order_id, mail)
        return_command = self.GET_ORDER
        return await self.connection.fetchrow(return_command, order_id)

    async def update_code(self, order_id: int, code: int) -> list[int|str]:
        update_command = self.UPDATE_CODE
        await self.connection.fetchval(update_command, order_id, code)
        return_command = self.GET_ORDER
        return await self.connection.fetchrow(return_command, order_id)

    async def get_order_date(self, order_id: int) -> datetime.datetime:
        command = self.GET_ORDER_DATE
        return await self.connection.fetchval(command, order_id)

    async def update_status(self, order_id: int, status: str) -> Record:
        command = self.UPDATE_STATUS
        return await self.connection.fetchrow(command, order_id, status)

<<<<<<< HEAD
    async def insert_games(self):
        if not await self.connection.fetchval(self.CHECK_GAMES):
            command = self.INSERT_GAMES
            values = [
                ('Brawl Stars',),
                ('Clash Royale',),
                ('Clash of Clans',)
            ]
            await self.connection.executemany(command, values)
        else:
            return True

    async def check_goods(self):
        command = self.CHECK_GOODS
        return await self.connection.fetchval(command)

    async def insert_goods(self):
        command = "INSERT INTO Goods(title, price, game_id) VALUES($1, $2, $3)"
        values = [
            ("30 гемов", 110, 1),
            ("80 гемов", 220, 1),
            ("170 гемов", 470, 1),
            ("360 гемов", 870, 1),
            ("950 гемов", 1900, 1),
            ("2000 гемов", 4200, 1),
            ("80 гемов", 55, 2),
            ("500 гемов", 220, 2),
            ("1200 гемов", 470, 2),
            ("2500 гемов", 820, 2),
            ("6500 гемов", 1900, 2),
            ("14000 гемов", 4000, 2),
            ("Pass Royale", 220, 2),
            ("80 гемов", 55, 3),
            ("500 гемов", 220, 3),
            ("1200 гемов", 470, 3),
            ("2500 гемов", 820, 3),
            ("6500 гемов", 1900, 3),
            ("14000 гемов", 4000, 3),
            ("Золотой пропуск", 220, 3)
        ]
        await self.connection.executemany(command, values)
=======
    async def check_ref_link(self, link: str) -> bool:
        command = self.CHECK_LINK_EXISTS
        return await self.connection.fetchval(command, link)

    async def update_reflink(self, link):
        command = self.UPDATE_REFLINK
        user_id = User.get_current().id
        return await self.connection.fetchval(command, user_id, link)

    async def get_ref_link(self):
        user_id = User.get_current().id
        command = self.GET_LINK
        return await self.connection.fetchval(command, user_id)
>>>>>>> 58dffac861a8537299080b7ff803537d3c9d01bf
