import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()

async def main():
    bot = Bot(os.getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    dp.message.middleware(ChatActionMiddleware())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

