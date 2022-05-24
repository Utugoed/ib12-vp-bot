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
    choose_sbj_kb = await get_choose_sbj_kb()
    if choose_sbj_kb is None:
        await message.answer(
            text="Пока что ни один предмет не был создан", reply_markup=main_keyboard
        )
    else:
        await message.answer(
            text="Выберите интересующий вас предмет", reply_markup=choose_sbj_kb
        )


@dp.callback_query_handler(Text(startswith="chs_sbj "))
async def choose_sbj(callback: types.CallbackQuery):
    subject = callback.data.replace("chs_sbj ", "")
    await callback.message.answer(
        text="Что вы хотите сделать?",
        reply_markup=await get_choose_action_kb(subject),
    )
    await callback.answer()


# Добавление файлов------------------------------------------------------------------
class FSMUploadFiles(StatesGroup):
    get_file = State()


@dp.callback_query_handler(Text(startswith="upload_files "), state="*")
async def waiting_files_to_upload(callback: types.CallbackQuery, state: FSMContext):
    await FSMUploadFiles.get_file.set()
    subject = callback.data.replace("upload_files ", "")
    await state.update_data(subject=subject)
    await callback.message.answer(
        "Пришлите сообщения, которые вы хотите сохранить.\
         \nКогда все файлы будут отправлены нажмите 'Готово'",
        reply_markup=await get_upload_kb(),
    )
    await callback.answer()


@dp.message_handler(text="Отмена", state=FSMUploadFiles.get_file)
async def cancel_upload(message: types.Message, state: FSMContext):
    await message.answer("Загрузка отменена", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(text="Готово", state=FSMUploadFiles.get_file)
async def complete_upload(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject_id = await Subjects.get_subject_id(data["subject"])
    input_data = {"subject_id": subject_id}
    if "msgs" in data.keys():
        input_data.update({"msgs": data["msgs"]})
    if "photos" in data.keys():
        input_data.update({"photos": data["photos"]})
    if input_data == {"subject_id": subject_id}:
        await message.answer(
            "Я не получил ни одного сообщения", reply_markup=main_keyboard
        )
    else:
        await Files.insert_files(input_data)
        await message.answer("Сообщения сохранены", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(state=FSMUploadFiles.get_file)
async def upload_message(message: types.Message, state: FSMContext):
    print()
    print(message)
    print()
    data = await state.get_data()
    if "msgs" in data.keys():
        files = data["msgs"]
    else:
        files = []
    files.append(message.text)
    await state.update_data(msgs=files)


@dp.message_handler(state=FSMUploadFiles.get_file, content_types="photo")
async def upload_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "photos" in data.keys():
        files = data["photos"]
    else:
        files = []
    print()
    print(message)
    print()
    files.append([message.photo[-1].file_id, message.photo[-1].file_unique_id])
    await state.update_data(photos=files)


# Получение файлов-----------------------------------------------------------------------
@dp.callback_query_handler(Text(startswith="get_files "))
async def get_sbj_files(callback: types.CallbackQuery):
    subject = callback.data.replace("get_files ", "")
    subject_id = await Subjects.get_subject_id(subject)
    files_list = await Files.get_files(subject_id)
    if files_list == []:
        await callback.answer("Сохраненных сообщений нет")
    else:
        for file in files_list:
            if "message_text" in file.keys():
                await dp.bot.send_message(
                    chat_id=callback.from_user.id, text=file["message_text"]
                )
            if "photo_id" in file.keys():
                await dp.bot.send_photo(
                    chat_id=callback.from_user.id, photo=file["photo_id"]
                )
        await callback.answer()


# Удаление файлов------------------------------------------------------------------------
class FSMDeleteFiles(StatesGroup):
    get_file = State()


@dp.callback_query_handler(Text(startswith="delete_files "), state="*")
async def waiting_for_files_to_delete(callback: types.CallbackQuery, state: FSMContext):
    await FSMDeleteFiles.get_file.set()
    subject = callback.data.replace("delete_files ", "")
    await state.update_data(subject=subject)
    await callback.message.answer(
        "Пришлите сообщения, которые вы хотите удалить.\
         \nКогда все файлы будут отправлены нажмите 'Готово'",
        reply_markup=await get_upload_kb(),
    )
    await callback.answer()


@dp.message_handler(text="Отмена", state=FSMDeleteFiles.get_file)
async def cancel_deleting(message: types.Message, state: FSMContext):
    await message.answer("Загрузка отменена", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(text="Готово", state=FSMDeleteFiles.get_file)
async def complete_deleting(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject_id = await Subjects.get_subject_id(data["subject"])
    input_data = {"subject_id": subject_id}
    if "msgs" in data.keys():
        input_data.update({"msgs": data["msgs"]})
    if "photos" in data.keys():
        input_data.update({"photos": data["photos"]})
    if input_data == {"subject_id": subject_id}:
        await message.answer(
            "Я не получил ни одного сообщения", reply_markup=main_keyboard
        )
    else:
        await Files.delete_files(input_data)
        await message.answer("Сообщения удалены", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(state=FSMDeleteFiles.get_file)
async def upload_message_to_delete(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "msgs" in data.keys():
        files = data["msgs"]
    else:
        files = []
    files.append(message.text)
    await state.update_data(msgs=files)


@dp.message_handler(state=FSMDeleteFiles.get_file, content_types="photo")
async def upload_photo_to_delete(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "photos" in data.keys():
        files = data["photos"]
    else:
        files = []
    files.append(message.photo[-1].file_unique_id)
    await state.update_data(photos=files)
