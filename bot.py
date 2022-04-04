from aiogram.utils.executor import start_webhook

from app import config
from app.handlers import dp
from app.loader import bot


async def on_startup():
    bot.set_webhook(config.WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == "__main__":
    start_webhook(
        dispatcher = dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
