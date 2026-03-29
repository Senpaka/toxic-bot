from aiogram import Router
from aiogram.types import Message, MessageReactionUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import async_session
from db.crud.messages import add_message, get_message
from db.crud.user_reactions import delete_user_reactions, create_user_reactions
from db.crud.users import get_user_by_id

import logging

from db.models import UserBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message_reaction()
async def message_reaction( session_data: MessageReactionUpdated):

    tg_user = session_data.user
    user_id = tg_user.id
    message_id = session_data.message_id
    reactions = [r.emoji for r in session_data.new_reaction if r.type == "emoji"]

    async with async_session() as session:
        user = await get_user_by_id(user_id, session)

        if not user:
            user = UserBase(
                tg_id=user_id,
                username=tg_user.username,
                role="user"
            )
            session.add(user)
            await session.flush()

        message = await get_message(message_id, session)

        if message:
            await delete_user_reactions(session, user.id, message.id)
            if reactions:
                await create_user_reactions(session, user.id, message.id, reactions)
        else:
            logger.warning("Message not found")
            raise TypeError("Message not found")


@router.message()
async def echo_handler(message: Message):
    """
    Метод для сохранения сообщений в бд
    :param message: сообщение
    """
    async with async_session() as session:
        try:
            db_msg = await add_message(session, message)

            logger.info(db_msg)
        except Exception as e:
            logger.warning(f"Ошибка сохранения сообщения: {e}")