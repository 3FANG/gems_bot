import os

from aiogram.types import Message
from aiogram.types.input_file import InputFile

from bot.database import Database

async def upload_photos(db: Database, message: Message):
    is_upload = await db.check_photo()
    if not is_upload:
        files_names = os.listdir(os.path.join('bot', 'photo'))
        for file_name in files_names:
            file_path = os.path.join(os.getcwd(), 'bot', 'photo', file_name)
            file = InputFile(file_path)
            update = await message.answer_photo(photo=file)
            res = await db.add_photo(photo_id=update.photo[-1].file_id,
                photo_unique_id=update.photo[-1].file_unique_id,
                file_path=file_path,
                game=file_name.split('.')[0])
    else:
        return True
