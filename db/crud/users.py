from aiogram import types
from aiogram.types import Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Any, Coroutine
from dotenv import load_dotenv
import os

from db.models import *

load_dotenv()
OWNER_ID = os.getenv("OWNER_BOT_ID")

async def add_user(user: UserBase, session: AsyncSession) -> None:
    session.add(user)
    await session.commit()

async def delete_user(user: UserBase, session: AsyncSession) -> None:
    await session.delete(user)
    await session.commit()

async def update_user(user: UserBase, session: AsyncSession) -> None:
    await session.merge(user)
    await session.commit()

async def get_user_by_id(user_id: int, session: AsyncSession) -> UserBase | None:
    statement = select(UserBase).where(UserBase.tg_id == user_id)
    result = await session.execute(statement)

    return result.scalar_one_or_none()

async def get_user_by_username(username: str, session: AsyncSession) -> Sequence[UserBase]:
    statement = select(UserBase).where(UserBase.username == username)
    result = await session.execute(statement)

    return result.scalars().all()

async def get_admin_users(session: AsyncSession) -> Sequence[UserBase]:
    statement = select(UserBase).where(UserBase.role == "admin")
    result = await session.execute(statement)

    return result.scalars().all()






