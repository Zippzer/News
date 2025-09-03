from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Создать пост"),
        KeyboardButton(text="Удалить пост"),
        KeyboardButton(text="Обновить пост")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)