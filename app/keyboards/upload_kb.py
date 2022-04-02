from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_upload_kb():
    upload_kb = InlineKeyboardMarkup(row_width=1)
    ready_btn = InlineKeyboardButton(
        text="Готово", callback_data="ready"
    )
    cancel_btn = InlineKeyboardButton(
        text="Отмена", callback_data="cancel"
    )
    upload_kb.add(ready_btn).add(cancel_btn)
    return upload_kb