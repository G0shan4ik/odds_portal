from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.types import Message

from .core import bot_, router
from .texts import ADD_USERS_TEXT, SEND_BETTER_NAME_TEXT, CHANGE_LIST_TEXT, NO_INSTALLED_BETTORS_TEXT
from .keyboard import exit_kb, in_list_kb, start_kb
from .states import CatchData
from .helpers import get_all_data, check_current_keywords, check_current_roi


@router.message(F.text == ADD_USERS_TEXT)
async def catch_nickname(message: Message, state: FSMContext):
    await message.answer(text=SEND_BETTER_NAME_TEXT, reply_markup=exit_kb())

    await state.set_state(CatchData.add_nickname)


@router.message(F.text == CHANGE_LIST_TEXT)
async def catch_nickname(message: Message):
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    all_data: list[list] = get_all_data(user_id=message.from_user.id)
    print(all_data)
    if not all_data:
        await message.answer(
            text=NO_INSTALLED_BETTORS_TEXT,
            reply_markup=start_kb()
        )
        return
    await message.answer(hbold('Вот список ваших бетторов ⬇️'))
    for data in all_data:
        await message.answer(
            text=f'{hbold("👤 Bettors name:  ")}{hbold(data[0])}.\n' \
                 f'''{hbold("• Keywords:  ")}{" + ".join([', '.join(item) for item in data[-1]]) if check_current_keywords(user_id=message.from_user.id ,name=data[0]) else "No KEYWORDS."}\n''' \
                 f'{hbold("• ROI:  ")}{data[1] if check_current_roi(user_id=message.from_user.id ,name=data[0]) else "No ROI."}',
            reply_markup=in_list_kb(name=data[0]),
        )

    await message.answer(f'Общее количество бетторов = {len(all_data)}')

