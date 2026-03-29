from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from bot.utils.callbacks import MarkAction


def get_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Получить сообщение для оценки",
        callback_data="get_message_to_mark"
    )

    return builder.as_markup()

def get_mark_kb(msg_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Полезный",
        callback_data=MarkAction(message_id=msg_id, label="useful")
    )

    builder.button(
        text="Токсичный",
        callback_data=MarkAction(message_id=msg_id, label="toxic")
    )

    builder.button(
        text="Нейтральный",
        callback_data=MarkAction(message_id=msg_id, label="neutral")
    )

    builder.adjust(1)
    return builder.as_markup()

def next_mark_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Стоп",
        callback_data="stop_marking"
    )

    builder.button(
        text="Делее",
        callback_data="get_message_to_mark"
    )

    return builder.as_markup()