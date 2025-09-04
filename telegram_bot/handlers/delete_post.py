from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,CallbackQuery
import httpx


delete_router = Router()


@delete_router.message(F.text == 'Удалить пост')
async def delete_handler(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/posts/")
        if response.status_code != 200:
            await message.answer("Ошибка при получении списка постов")
            return

        data = response.json()
        kb = InlineKeyboardBuilder()

        for item in data:
            kb.row(
                InlineKeyboardButton(
                    text=f"{item['topic']}",
                    callback_data=f"edit_{item['id']}"
                )
            )
        await message.answer(
            "Выберите статью для удаления:",
            reply_markup=kb.as_markup()
        )

