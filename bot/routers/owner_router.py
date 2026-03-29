from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message


from sqlalchemy import select, update

from db.engine import async_session
from db.models import UserBase
from bot.filtters.admin_filter import AdminFilter

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("set_role"), AdminFilter())
async def set_user_role(message: Message, command: CommandObject):
    role = command.args
    logger.info(f"Setting role: {role}")

    if not role:
        return await message.answer("Ошибка! Напиши /set_role <role_name>")

    async with async_session() as session:

        statement = select(UserBase).where(UserBase.tg_id == message.from_user.id)
        result = await session.execute(statement)
        current_user = result.scalar_one_or_none()

        logger.info(f"Current user: {current_user.username}, role: {current_user.role}")

        if not current_user or current_user.role != "owner":
            return await message.answer("У тебя нет прав что бы сделать это!")

        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id

            statement = update(UserBase).where(UserBase.tg_id == target_id).values(role=role)
            await session.execute(statement)
            await session.commit()

            await message.answer(f"Пользователь {target_id} стал {role}")
        else:
            await message.answer(f"Нужно переслать сообщение для этой команды")

    return None