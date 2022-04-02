from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.db.subjects import Subjects
from app.loader import dp


class FSMSbjCreate(StatesGroup):
    sbj_name = State()


@dp.message_handler(text="Добавить предмет")
async def create_subject(message: types.Message):
    await FSMSbjCreate.sbj_name.set()
    await message.answer(text="Напишите название предемета")


@dp.message_handler(state=FSMSbjCreate.sbj_name)
async def get_sbj_name(message: types.Message, state: FSMContext):
    sbj_list = [subject["name"].title() for subject in await Subjects.get_subjects()]
    if message.text.title() in sbj_list:
        await message.answer(text="Этот предмет уже добавлен")
        await state.finish()
    else:
        await message.answer(
            text="Готово. Предмет " + message.text + " был успешно добавлен."
        )
        await state.finish()
