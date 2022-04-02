from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.db.subjects import Subjects
from app.keyboards.choose_sbj_kb import get_choose_sbj_kb, get_choose_action_kb
from app.keyboards.upload_kb import get_upload_kb
from app.loader import dp


@dp.message_handler(text="Список предметов")
async def subjects_list(message: types.Message):
    await message.answer(
        text="Выберите интересующий вас предмет", reply_markup=await get_choose_sbj_kb()
    )


@dp.callback_query_handler(Text(startswith="chs_sbj "))
async def choose_sbj_for_del(callback: types.CallbackQuery):
    subject = callback.data.replace("chs_sbj ", "")
    await callback.message.answer(
        text="Выберите интересующий вас предмет",
        reply_markup=await get_choose_action_kb(subject),
    )

class FSMUploadFiles(StatesGroup):
    get_file = State()

@dp.callback_query_handler(Text(startswith="upload_files "), state="*")
async def choose_sbj_for_del(callback: types.CallbackQuery, state: FSMContext):
    await FSMUploadFiles.get_file.set()
    subject = callback.data.replace("upload_files ", "")
    await state.update_data(subject=subject,files=[])

@dp.message_handler(state=FSMUploadFiles.get_file)
async def upload_files(message: types.Message, state: FSMContext):
    data = await state.get_data()
    files = data["files"]
    files = files.append(message.message_id)
    await message.answer("Это все сообщения?", reply_markup=await get_upload_kb())

@dp.callback_query_handler(Text(startswith="cancel"), state=FSMUploadFiles.get_file)
async def cancel_upload(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Загрузка отменена")
    await state.finish()

@dp.callback_query_handler(Text(startswith="ready"), state=FSMUploadFiles.get_file)
async def cancel_upload(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_id = await Subjects.get_subject_id(data["subject"])
    
    await callback.message.answer("Загрузка отменена")
    await state.finish()
