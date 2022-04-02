from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


choose_sbj_btn = KeyboardButton("Список предметов")
create_sbj_btn = KeyboardButton("Добавить предмет")
delete_sbj_btn = KeyboardButton("Удалить предмет")

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_keyboard.add(choose_sbj_btn).add(create_sbj_btn).insert(delete_sbj_btn)
