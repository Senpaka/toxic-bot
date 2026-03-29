from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filtters.admin_filter import AdminFilter
from bot.keyboards.inline import get_admin_kb

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("panel"), AdminFilter())
async def panel(message: Message):

    logger.info("Panel is draw")
    await message.answer(
        "Панель администратора:",
        reply_markup=get_admin_kb(),
    )