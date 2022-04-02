from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.db.subjects import Subjects


async def get_choose_sbj_kb():
    chs_sbj_kb = InlineKeyboardMarkup(row_width=1)
    sbj_list = [sbj["name"].title() for sbj in await Subjects.get_subjects()]
    btn_list = [
        InlineKeyboardButton(text=sbj, callback_data=f"chs_sbj {sbj}")
        for sbj in sbj_list
    ]
    chs_sbj_kb.add(*btn_list)
    return chs_sbj_kb


async def get_choose_action_kb(subject: str):
    chs_act_kb = InlineKeyboardMarkup(row_width=1)
    get_files_btn = InlineKeyboardButton(
        text="Просмотреть файлы", callback_data=f"get_files {subject}"
    )
    upload_files_btn = InlineKeyboardButton(
        text="Добавить файлы", callback_data=f"upload_files {subject}"
    )
    delete_files_btn = InlineKeyboardButton(
        text="Удалить файлы", callback_data=f"delete_files {subject}"
    )
    chs_act_kb.add(get_files_btn).row(upload_files_btn, delete_files_btn)
    return chs_act_kb
