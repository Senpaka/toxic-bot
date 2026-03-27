from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import *
from db.crud.users import get_user_by_id, add_user
from aiogram import types

async def add_message(
        session: AsyncSession,
        tg_msg: types.Message,
        model_label: str | None = None
) -> MessageBase:

    tg_user_id = tg_msg.from_user.id
    user = await get_user_by_id(tg_user_id, session)

    if not user:
        user = UserBase(
            tg_id=tg_user_id,
            username=tg_msg.from_user.username,
            role="user"
        )
        await add_user(user, session)

    message = MessageBase(
        tg_id=tg_msg.message_id,
        chat_id=tg_msg.chat.id,
        user_id=tg_user_id,
        content=tg_msg.text or "",
        created_at=tg_msg.date.replace(tzinfo=None),
        model_label=model_label
    )

    session.add(message)

    await session.commit()
    await session.refresh(message)

    return message

async def get_message(message_id: int, session: AsyncSession) -> MessageBase:

    statement = select(MessageBase).where(MessageBase.id == message_id)
    result = await session.execute(statement)

    return result.scalar_one_or_none()