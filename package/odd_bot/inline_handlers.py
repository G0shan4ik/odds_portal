from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from .core import router, bot_, ADMIN_ID
from .helpers import delete_bettor, set_current_better, callback_on_off, check_current_roi
from .texts import WRONG_TEXT, SUCCESS_DELETING_BETTOR, ENTER_KEYS_TEXT, ENTER_ROI_TEXT
from .states import CatchData
from .keyboard import exit_kb, in_list_kb
from package.database import LinksBetters


@router.callback_query(lambda query: query.data.startswith('delete_better'))
async def del_bettor(query: CallbackQuery):
    user_id = query.from_user.id
    _bet_name = query.data.split('-')[-1]

    if not delete_bettor(user_id=user_id, name=_bet_name):
        await query.answer(text=WRONG_TEXT, show_alert=True)
        await bot_.send_message(chat_id=ADMIN_ID, text=WRONG_TEXT)
        return True

    await query.answer(SUCCESS_DELETING_BETTOR(_bet_name))

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )


@router.callback_query(lambda query: query.data.startswith('add_better_keywords'))
async def enter_keys(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    _bet_name = query.data.split('-')[-1]

    set_current_better(user_id=user_id, name=_bet_name)
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    await bot_.send_message(
        chat_id=user_id,
        text=ENTER_KEYS_TEXT(_bet_name),
        reply_markup=exit_kb()
    )
    await state.set_state(CatchData.enter_keys)


@router.callback_query(lambda query: query.data.startswith('st'))
async def on_off_callback(query: CallbackQuery):
    _name = query.data.split('-')[-1]
    if query.data.split('-')[0] == 'start' and not check_current_roi(user_id=query.from_user.id, name=_name):
        await query.answer(f'Укажите ROI для {_name}!!!', show_alert=True)
        return
    callback_on_off(better_nickname=_name, change=True)
    await bot_.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=in_list_kb(name=_name)
    )

@router.callback_query(lambda query: query.data.startswith('roi_better'))
async def catch_better_roi(query: CallbackQuery, state: FSMContext):
    name = query.data.split('-')[-1]
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await bot_.send_message(
        chat_id=query.from_user.id,
        text=ENTER_ROI_TEXT(name)
    )
    set_current_better(user_id=query.from_user.id, name=name)
    await state.set_state(CatchData.enter_roi)