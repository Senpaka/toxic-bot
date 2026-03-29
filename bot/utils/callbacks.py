from aiogram.filters.callback_data import CallbackData

class MarkAction(CallbackData, prefix="mark"):
    """
    Колбэк для пометки
    """
    message_id: int
    label: str
