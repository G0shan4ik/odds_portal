from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from .texts import ADD_USERS_TEXT, CHANGE_LIST_TEXT, MAIN_MENU_TEXT
from .helpers import callback_on_off


def start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADD_USERS_TEXT)],
            [KeyboardButton(text=CHANGE_LIST_TEXT)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def exit_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MAIN_MENU_TEXT)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def in_list_kb(name):
    clb = callback_on_off(better_nickname=name)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Enter ROI 📉', callback_data=f'roi_better-{name}'),
                InlineKeyboardButton(text='Enter keywords 📝', callback_data=f'add_better_keywords-{name}')
            ],
            [InlineKeyboardButton(text='Delete 🗑', callback_data=f'delete_better-{name}')],
            [InlineKeyboardButton(text=clb + ' ✅' if clb == 'Start' else clb + ' ❌', callback_data=f'{clb.lower()}-{name}')]
        ],
        resize_keyboard=True
    )