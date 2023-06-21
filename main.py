import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from handlers import router
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get('BOT_TOKEN'))

dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
