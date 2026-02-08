import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio

from bot_logic.handlers import handlers_router

load_dotenv()

async def start():
    bot = Bot(token=os.getenv("BOT_TOKEN")) # экземпляр ТГ бота
    dp = Dispatcher() # управляет запросами пользователя

    dp.include_router(handlers_router)

    try:
        await dp.start_polling(bot) # запускаем в работу другой асинхронный код
    finally:
        await bot.session.close() # закрывается соединение с сервером

if __name__ == '__main__': # проверка, что код выполняется из файла, а не и какого-то другого места
    asyncio.run(start())
