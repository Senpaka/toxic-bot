import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import os

from db.engine import async_session
from db.crud.messages import add_message

import logging

from bot.routers import admin_panel_router, marking_router, owner_router, fallback_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    logger.info("Запуск бота...")

    dp.include_router(admin_panel_router.router)
    dp.include_router(marking_router.router)
    dp.include_router(owner_router.router)
    dp.include_router(fallback_router.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopping bot...")

