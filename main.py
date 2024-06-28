import asyncio

import sys
import logging

from aiogram.methods import DeleteWebhook
from aiogram.utils.markdown import hbold

from package.database import init, Users
from package.odd_bot.core import bot_, dp
from package.parsers.main_parser import schedule


async def on_startup(dispatcher):
    for item in Users.select():
        await bot_.send_message(
            chat_id=749654188,
            text=hbold('Бот снова запущен!')
        )


async def on_shutdown(dispatcher):
    for item in Users.select():
        await bot_.send_message(
            chat_id=item.user_id,
            text=hbold('Бот остановлен 😥, дла проведения технических работ!\n'
                       'Это не займёт много времени)')
        )


async def main():
    await bot_(DeleteWebhook(drop_pending_updates=True))
    init()

    dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)
    await asyncio.gather(
        dp.start_polling(bot_),
        schedule()
    )


def start_dev():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())