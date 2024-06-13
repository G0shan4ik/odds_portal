import asyncio

import sys
import logging

from aiogram.methods import DeleteWebhook

from package.database import init
from package.odd_bot.core import bot_, dp
from package.parsers.main_parser import schedule


async def main():
    await bot_(DeleteWebhook(drop_pending_updates=True))
    init()
    await asyncio.gather(dp.start_polling(bot_), schedule())


def start_dev():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())