from package.database import *
from ast import literal_eval


def save_data_to_database(_user_id: int, nickname: str, link: str) -> LinksBetters:
    user_in: Users = Users.get_or_create(user_id=_user_id)[0]
    user: LinksBetters = LinksBetters.get_or_create(link=link, user_id=user_in, better_nickname=nickname)[0]

    return user


def delete_user_data(user_id: int, nickname: str) -> bool:
    try:
        LinksBetters.delete().where(LinksBetters.user_id == user_id, LinksBetters.nickname == nickname).execute()
        return True
    except Exception as ex:
        print(f'\n\nError deleting: {ex}\n\n')
        return False


def get_all_data(user_id: int) -> list[list]:
    _select = LinksBetters.select().where(LinksBetters.user == user_id)
    return [[item.better_nickname, item.roi, literal_eval(item.keyword)] for item in _select]


def check_current_keywords(user_id: int, name: str):
    _select = LinksBetters.select().where(
        LinksBetters.user == user_id,
        LinksBetters.better_nickname == name,
        LinksBetters.keyword != '[""]')
    return True if _select else False

def check_current_roi(user_id: int, name: str):
    _select = LinksBetters.select().where(
        LinksBetters.user == user_id,
        LinksBetters.better_nickname == name,
        LinksBetters.roi != -1111)
    return True if _select else False


def check_correct_bettors_name(user_id: int, name: str) -> bool:
    _select = LinksBetters.select().where(LinksBetters.user_id == user_id, LinksBetters.better_nickname == name)
    return True if _select.exists() else False

def delete_bettor(user_id: int, name: str):
    try:
        LinksBetters.delete().where(LinksBetters.user == user_id, LinksBetters.better_nickname == name).execute()
        return True
    except Exception as ex:
        print(f'\n\nError deleting: {ex}\n\n')
        return False


def add_keys(user_id: int, name: str, keys: str):
    try:
        user: LinksBetters = LinksBetters.get_or_create(user=user_id, better_nickname=name, current_better=True)[0]
        user.keyword = keys if keys != "[['1']]" else '[""]'
        user.save()
        return True
    except Exception as ex:
        print(f'\n\nError enter_keys: {ex}\n\n')
        return False


def set_current_better(user_id: int, name: str, t_or_f: bool = True):
    user: LinksBetters = LinksBetters.get_or_create(user_id=user_id, better_nickname=name, current_better=not t_or_f)[0]
    user.current_better = t_or_f
    user.save()
    return True

def return_bettors_name(user_id: int) -> str:
    user: LinksBetters = LinksBetters.get_or_create(user=user_id, current_better=True)[0]
    return user.better_nickname


def callback_on_off(better_nickname: str, change: bool = False):
    user: LinksBetters = LinksBetters.get_or_create(better_nickname=better_nickname)[0]
    if not change:
        return 'Stop' if user.on_off else 'Start'

    user.on_off = not user.on_off
    user.save()


def save_roi(user_id: int, roi: int) -> None:
    user: LinksBetters = LinksBetters.get_or_create(user=user_id, current_better=True)[0]
    user.roi = roi
    user.save()