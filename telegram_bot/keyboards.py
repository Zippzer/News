from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboards():
    buttons = [
        [KeyboardButton(text='Создать пост'), KeyboardButton(text='Отредактировать пост'),
         KeyboardButton(text='Удалить пост'), KeyboardButton(text="Обновить пост")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
