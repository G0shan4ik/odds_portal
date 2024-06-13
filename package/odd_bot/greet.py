from aiogram.filters import CommandStart
from aiogram.types import Message

from .core import dp
from .texts import START_TEXT
from .keyboard import start_kb


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(text=START_TEXT)
    await message.answer(
        text='✋',
        reply_markup=start_kb()
    )