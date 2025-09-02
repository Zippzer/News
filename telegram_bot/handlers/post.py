from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils import Post
import httpx
from datetime import datetime

create_router = Router()

@create_router.message(F.text == 'Создать пост')
async def create_post(message:Message,state:FSMContext):
    await message.answer('Введите название статьи')
    await state.set_state(Post.topic)


@create_router.message(state=Post.topic)
async def set_url(message:Message,state:FSMContext):
    await state.update_data(topic=message.text)
    await message.answer('Введите ссылку на дашборд')
    await state.set_state(Post.dashboard_url)


@create_router.message(state=Post.dashboard_url)
async def set_dashboard_url(message:Message,state:FSMContext):
    await state.update_data(dashboard_url=message.text)
    await message.answer('Введите показатели дашборда')
    await state.set_state(Post.indicators)


@create_router.message(state=Post.indicators)
async def set_indicators(message:Message,state:FSMContext):
    await state.update_data(indicators=message.text)
    await state.set_state(Post.date)


@create_router.message(state=Post.date)
async def set_date_end(message: Message, state: FSMContext):
    await state.update_data(date=datetime.now())
    data = await state.get_data()
    await state.clear()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/posts/create",
                json=data
            )
        if response.status_code == 200:
            await message.answer("Данные успешно сохранены")
        else:
            await message.answer(f"Ошибка сервера: {response.status_code}")

    except httpx.RequestError as e:
        await message.answer("Не удалось подключиться к серверу")
    except Exception as e:
        await message.answer("Произошла ошибка при отправке данных")





