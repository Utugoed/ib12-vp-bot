from aiogram import types
from aiogram.dispatcher.filters import Text

from app.db.subjects import Subjects
from app.keyboards.del_kb import get_delete_kb
from app.loader import dp


@dp.message_handler(text="Удалить предмет")
async def delete_subject(message: types.Message):
    delete_sbj_kb = await get_delete_kb()
    await message.answer(
        text="Выберите предмет, который хотите удалить:", reply_markup=delete_sbj_kb
    )


@dp.callback_query_handler(Text(startswith="del_sbj "))
async def choose_sbj_for_del(callback: types.CallbackQuery):
    subject = callback.data.replace("del_sbj ", "")
    await Subjects.delete_subject(name=subject)
    await callback.answer("Предмет " + subject + " был удален")
