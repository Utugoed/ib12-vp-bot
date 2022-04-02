from aiogram import types

from app.keyboards import main_keyboard
from app.loader import dp


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        text="Привет, я - бот для загрузки файлов группы ИБ-12вп",
        reply_markup=main_keyboard,
    )
