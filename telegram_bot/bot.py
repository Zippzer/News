import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from keyboards import main_menu_keyboards


load_dotenv()
API_TOKEN = os.getenv('TOKEN_BOT')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message:types.Message):
    await message.answer('Выберите действие', reply_markup=main_menu_keyboards())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())