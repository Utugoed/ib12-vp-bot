from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.db.files import Files
from app.db.subjects import Subjects
from app.keyboards.choose_sbj_kb import get_choose_sbj_kb, get_choose_action_kb
from app.keyboards.main_kb import main_keyboard
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
        text="Что вы хотите сделать?",
        reply_markup=await get_choose_action_kb(subject),
    )

#Добавление файлов------------------------------------------------------------------
class FSMUploadFiles(StatesGroup):
    get_file = State()

@dp.callback_query_handler(Text(startswith="upload_files "), state="*")
async def choose_sbj_for_del(callback: types.CallbackQuery, state: FSMContext):
    await FSMUploadFiles.get_file.set()
    subject = callback.data.replace("upload_files ", "")
    await state.update_data(subject=subject)
    await callback.message.answer("Пришлите сообщения, которые вы хотите сохранить.\
         \nКогда все файлы будут отправлены нажмите 'Готово'", 
         reply_markup=await get_upload_kb())

@dp.message_handler(text="Отмена", state=FSMUploadFiles.get_file)
async def cancel_upload(message: types.Message, state: FSMContext):
    await message.answer("Загрузка отменена", reply_markup=main_keyboard)
    await state.finish()

@dp.message_handler(text='Готово', state=FSMUploadFiles.get_file)
async def complete_upload(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject_id = await Subjects.get_subject_id(data["subject"])
    input_data = {"subject_id": subject_id}
    if "msgs" in data.keys():
        input_data.update({"msgs": data["msgs"]})
    if "photos" in data.keys():
        input_data.update({"photos": data["photos"]})
    await Files.insert_files(input_data)
    await message.answer("Сообщения сохранены", reply_markup=main_keyboard)
    await state.finish()

@dp.message_handler(state=FSMUploadFiles.get_file)
async def upload_files(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "msgs" in data.keys():
        files = data["msgs"]
    else:
        files = []
    files.append(message.text)
    await state.update_data(msgs=files)

@dp.message_handler(state=FSMUploadFiles.get_file, content_types="photo")
async def upload_files(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "photos" in data.keys():
        files = data["photos"]
    else:
        files = []
    files.append(message.photo[-1].file_id)
    await state.update_data(photos=files)

#Получение файлов-----------------------------------------------------------------------
@dp.callback_query_handler(Text(startswith="get_files "))
async def choose_sbj_for_del(callback: types.CallbackQuery):
    subject = callback.data.replace("get_files ", "")
    subject_id = await Subjects.get_subject_id(subject)
    files_list = await Files.get_files(subject_id)
    for file in files_list:
        if "message_text" in file.keys():
            await dp.bot.send_message(chat_id=callback.from_user.id, text=file["message_text"])
        if "photo_id" in file.keys():
            await dp.bot.send_photo(chat_id=callback.from_user.id, photo=file["photo_id"])