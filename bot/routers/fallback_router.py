from aiogram import Router
from aiogram.types import Message

from db.engine import async_session
from db.crud.messages import add_message

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def echo_handler(message: Message):
    async with async_session() as session:
        try:
            db_msg = await add_message(session, message)

            logger.info(db_msg)
        except Exception as e:
            logger.warning(f"Ошибка сохранения сообщения: {e}")