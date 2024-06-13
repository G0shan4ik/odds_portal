import asyncio

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from .core import router
from .keyboard import start_kb, exit_kb
from .texts import (
    SUCCESS_TEXT,
    MAIN_MENU_TEXT,
    WRONG_TEXT,
    SUCCESS_ENTER_KEYS_TEXT,
    SUCCESS_DELETE_KEYS_TEXT,
    SUCCESS_SAVE_ROI,
    UNSUCCESS_SAVE_ROI,
    WRONG_BETTORS_NAME
)
from .helpers import save_data_to_database, set_current_better, add_keys, return_bettors_name, save_roi, check_correct_bettors_name


class CatchData(StatesGroup):
    add_nickname = State()
    enter_keys = State()
    enter_roi = State()


@router.message(F.text == MAIN_MENU_TEXT)  # exit the state
async def exit_the_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вурнулись в главное меню 🏠',
        reply_markup=start_kb()
    )
    await state.clear()


@router.message(CatchData.add_nickname, F.text)
async def state_add_nickname(message: Message, state: FSMContext):
    _name = message.text

    if check_correct_bettors_name(user_id=message.from_user.id, name=_name):
        await message.answer(text=WRONG_BETTORS_NAME(_name), reply_markup=exit_kb())
        return

    _link = f'https://www.oddsportal.com/profile/{_name}/my-predictions/next/'
    if not save_data_to_database(_user_id=message.from_user.id, nickname=_name, link=_link):
        await message.answer(text=WRONG_TEXT)
        return

    txt = 'Загрузка'
    s = ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌑']
    message = await message.answer(txt)
    for i in range(1, 14):
        txt += s[i-1]
        await asyncio.sleep(0.01)
        await message.edit_text(text=txt)
        txt = 'Загрузка'

    await message.answer(SUCCESS_TEXT(_name), reply_markup=start_kb())
    await state.clear()


@router.message(CatchData.enter_keys, F.text)
async def state_enter_keywords(message: Message, state: FSMContext):
    _name = return_bettors_name(message.from_user.id)
    _keys: list = message.text.replace(' ', '').split(',')

    add_keys(user_id=message.from_user.id, name=_name, keys=_keys)
    set_current_better(user_id=message.from_user.id, name=_name, t_or_f=False)
    await message.answer(
        text=SUCCESS_ENTER_KEYS_TEXT(_name) if _keys[0] != '1' else SUCCESS_DELETE_KEYS_TEXT(_name),
        reply_markup=start_kb()
    )
    await state.clear()


@router.message(CatchData.enter_roi, F.text)
async def state_enter_roi(message: Message, state: FSMContext):
    if message.text.isdigit():
        save_roi(user_id=message.from_user.id, roi=int(message.text))

        _name = return_bettors_name(message.from_user.id)
        set_current_better(user_id=message.from_user.id, name=_name, t_or_f=False)

        await message.answer(text=SUCCESS_SAVE_ROI, reply_markup=start_kb())
        await state.clear()
        return
    await message.answer(text=UNSUCCESS_SAVE_ROI)
    await state.set_state(CatchData.enter_roi)
