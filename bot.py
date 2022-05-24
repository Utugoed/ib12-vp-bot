from aiogram import executor
from aiogram.utils.executor import start_webhook

from app import config
from app.db.connection import connect_to_mongodb, close_mongodb_connection
from app.handlers import dp
from app.loader import bot


async def on_startup(dispatcher):
    await connect_to_mongodb()
    # await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await close_mongodb_connection()
    # await bot.delete_webhook()


if __name__ == "__main__":
    # start_webhook(
    #     dispatcher = dp,
    #     webhook_path=config.WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=config.WEBAPP_HOST,
    #     port=config.WEBAPP_PORT,
    # )
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True
    )
