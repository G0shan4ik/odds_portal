from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os


load_dotenv()

TOKEN_API = os.getenv('TOKEN_API')
ADMIN_ID = os.getenv('ADMIN_ID')

bot_ = Bot(
    token=TOKEN_API,
    parse_mode=ParseMode.HTML
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)