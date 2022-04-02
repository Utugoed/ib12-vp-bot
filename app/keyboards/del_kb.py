from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.db.subjects import Subjects


async def get_delete_kb():
    delete_kb = InlineKeyboardMarkup(row_width=1)
    sbj_list = [sbj["name"].title() for sbj in await Subjects.get_subjects()]
    btn_list = [
        InlineKeyboardButton(text=sbj, callback_data=f"del_sbj {sbj}")
        for sbj in sbj_list
    ]
    delete_kb.add(*btn_list)
    return delete_kb
