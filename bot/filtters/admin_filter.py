from aiogram import types
from aiogram.filters import BaseFilter
from sqlalchemy import select

from db.engine import async_session
from db.models import UserBase


class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        async with async_session() as session:
            statement = select(UserBase).where(UserBase.tg_id == message.from_user.id)
            result = await session.execute(statement)
            user = result.scalar_one_or_none()

            return user is not None and user.role in ["admin", "owner"]