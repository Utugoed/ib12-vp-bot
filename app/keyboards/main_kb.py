from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


upload_btn = KeyboardButton("/upload")
download_btn = KeyboardButton("/download")
create_sbj_btn = KeyboardButton("/create_sbj")
delete_sbj_btn = KeyboardButton("/delete_sbj")

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_keyboard.add(upload_btn).insert(download_btn).add(create_sbj_btn).insert(delete_sbj_btn)