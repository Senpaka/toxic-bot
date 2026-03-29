from aiogram.filters.callback_data import CallbackData


class MarkAction(CallbackData, prefix="mark"):
    message_id: int
    label: str
