from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery


from sqlalchemy import select, update, func

from db.engine import async_session
from db.models import UserBase, MessageBase
from bot.filtters.admin_filter import AdminFilter
from bot.utils.callbacks import MarkAction

import logging

from bot.keyboards.inline import get_mark_kb, next_mark_kb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(lambda c: c.data == "get_message_to_mark", AdminFilter())
async def get_message_to_mark(callback: CallbackQuery):
    logger.info(f"Getting message to mark: {callback.data}")
    async with async_session() as session:
        logger.info("Finding random unmarked message")
        statement = (
            select(MessageBase)
            .where(MessageBase.final_label.is_(None))
            .order_by(func.random())
            .limit(1)
        )
        result = await session.execute(statement)
        message = result.scalar_one_or_none()

        if message:

            statement = (
                select(UserBase)
                .where(UserBase.tg_id == message.user_id)
            )
            result = await session.execute(statement)
            user = result.scalar_one_or_none()

            if message.file_id:
                logger.info(f"Send message with photo")
                await callback.message.answer_photo(
                    photo=message.file_id,
                    caption=f"Сообщение для разметки:\nОтправил: {user.username}\nСообщение: {message.content}",
                    reply_markup=get_mark_kb(message.id)
                )
            else:
                logger.info(f"Send message")
                await callback.message.answer(
                    text=f"Сообщение для разметки:\nОтправил: {user.username}\nСообщение: {message.content}",
                    reply_markup=get_mark_kb(message.id)
                )

        else:
            logger.info(f"Message is end")
            await callback.message.answer(
                "Сообщения для разметки закончились(("
            )

        await callback.answer()

@router.callback_query(MarkAction.filter())
async def set_mark(callback: CallbackQuery, callback_data: MarkAction):
    message_id = callback_data.message_id
    label = callback_data.label

    logger.info(f"Setting mark: {label}")

    async with async_session() as session:
        stmt = (
            update(MessageBase)
            .where(MessageBase.id == message_id)
            .values(final_label=label)
        )
        await session.execute(stmt)
        await session.commit()

    readable_labels = {
        "useful": "Полезный",
        "toxic": "Токсичный",
        "neutral": "Нейтральный"
    }

    new_text = (
        f" Сообщение #{message_id} размечено.\n"
        f"Итог: **{readable_labels.get(label)}**"
    )

    if callback.message.photo:
        await callback.message.edit_caption(
            caption=new_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=next_mark_kb()
        )
    else:
        await callback.message.edit_text(
            text=new_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=next_mark_kb()
        )

    await callback.answer()

@router.callback_query(lambda c: c.data == "stop_marking")
async def stop_marking(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Работа завершена. Спасибо!")
    await callback.answer()