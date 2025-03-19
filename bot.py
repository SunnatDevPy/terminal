import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from models.database import db
from start import start_router

API_TOKEN = "7976782172:AAGB3k4LMCx4pwIRsauYc_eWKnHZ1WpBPZE"
GROUP_ID = -1002279369370


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def on_start(bot: Bot):
    await db.create_all()


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_start)
    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())
