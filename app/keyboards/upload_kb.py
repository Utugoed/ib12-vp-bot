from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def get_upload_kb():
    upload_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    ready_btn = KeyboardButton(text="Готово")
    cancel_btn = KeyboardButton(text="Отмена")
    upload_kb.add(ready_btn).add(cancel_btn)
    return upload_kb
