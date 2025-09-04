import httpx
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,CallbackQuery
from utils import UpdatePost


news_router = Router()


@news_router.message(F.text == 'Обновить пост')
async def list_post(message: Message):
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
            "Выберите статью для редактирования:",
            reply_markup=kb.as_markup()
        )


@news_router.callback_query(F.data.startswith('edit'))
async def handle_button_click(callback: CallbackQuery):
    post_id = callback.data
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/posts/{post_id}")
        if response.status_code != 200:
            await callback.answer("Ошибка при получении поста", show_alert=True)
            return
        data = response.json()

        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Тема", callback_data=f"field_topic_{post_id}"))
        kb.row(InlineKeyboardButton(text="Дашборд", callback_data=f"field_dashboard_{post_id}"))
        kb.row(InlineKeyboardButton(text="URL дашборда", callback_data=f"field_dashboard_url_{post_id}"))
        kb.row(InlineKeyboardButton(text="Индикаторы", callback_data=f"field_indicators_{post_id}"))
        kb.row(InlineKeyboardButton(text="Дата", callback_data=f"field_date_{post_id}"))
        kb.row(InlineKeyboardButton(text="Удалить пост", callback_data=f"delete_{post_id}"))
        kb.row(InlineKeyboardButton(text="Назад к списку", callback_data="back_to_list"))

        post_info = (
            f"Пост ID: {data['id']}\n"
            f"Тема: {data['topic']}\n"
            f"Дашборд: {data['dashboard'] or 'Не указано'}\n"
            f"URL: {data['dashboard_url'] or 'Не указано'}\n"
            f"Индикаторы: {data['indicators'] or 'Не указано'}\n"
            f"Дата: {data['date']}\n\n"
            f"Выберите что хотите изменить:"
        )

        await callback.message.edit_text(
            post_info,
            reply_markup=kb.as_markup()
        )
        await callback.answer()


@news_router.callback_query(F.data.startswith('field'))
async def handle_field_update(callback: CallbackQuery, state: FSMContext):
    data_arr = callback.data.split('_')
    field_type = data_arr[1]
    post_id = data_arr[2]

    await state.set_state(UpdatePost.waiting_field_value)

    field_names = {
        'topic': 'тему поста',
        'dashboard': 'название дашборда',
        'url': 'URL дашборда',
        'indicators': 'индикаторы',
        'date': 'дату (ГГГГ-ММ-ДД)'
    }

    await callback.message.edit_text(f"Введите {field_names[field_type]}:")
    await callback.answer()


@news_router.message(UpdatePost.waiting_field_value, F.text)
async def process_field_update(message: Message, state: FSMContext):
    data = await state.get_data()
    field_type = data['field']
    post_id = data['post_id']

    field_map = {
        'topic': 'topic',
        'dashboard': 'dashboard',
        'url': 'dashboard_url',
        'indicators': 'indicators',
        'date': 'date'
    }

    db_field = field_map[field_type]
    update_data = {db_field: message.text}

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"http://localhost:8000/posts/{post_id}",
            json=update_data
        )

        if response.status_code == 200:
            await message.answer("Успешно обновлено!")
        else:
            await message.answer("Ошибка при обновлении")

    await state.clear()
