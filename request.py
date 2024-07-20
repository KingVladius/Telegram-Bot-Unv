import logging
import asyncio

from aiogram import Dispatcher
from config import bot
from Tg_bot.Main import router
from Tg_bot.Database.Models import async_main

dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # При виведенні з розробки виключить !!!
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit') 