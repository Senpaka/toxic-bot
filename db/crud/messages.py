from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import *
from db.crud.users import get_user_by_id, add_user
from aiogram import types
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def add_message(
        session: AsyncSession,
        tg_msg: types.Message,
        model_label: str | None = None
) -> MessageBase:

    tg_user_id = tg_msg.from_user.id
    user = await get_user_by_id(tg_user_id, session)

    logger.info("Adding message")

    if not user:
        user = UserBase(
            tg_id=tg_user_id,
            username=tg_msg.from_user.username,
            role="user"
        )
        session.add(user)
        await session.flush()

    photo_id = None

    if tg_msg.photo:
        photo_id = tg_msg.photo[-1].file_id

    message = MessageBase(
        tg_id=tg_msg.message_id,
        chat_id=tg_msg.chat.id,
        user_id=user.id,
        content=tg_msg.text or tg_msg.caption or "",
        file_id=photo_id,
        created_at=tg_msg.date.replace(tzinfo=None),
        model_label=model_label
    )

    session.add(message)

    await session.commit()
    await session.refresh(message)

    return message

async def get_message(message_id: int, session: AsyncSession) -> MessageBase:

    statement = select(MessageBase).where(MessageBase.tg_id == message_id)
    result = await session.execute(statement)

    return result.scalar_one_or_none()