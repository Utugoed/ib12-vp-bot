from aiogram.utils import executor

from app.handlers import dp


executor.start_polling(dp, skip_updates=True)