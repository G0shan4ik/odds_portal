import re
from datetime import datetime, timedelta
from time import sleep

from botasaurus import AntiDetectDriver

import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from random import uniform
from googletrans import Translator
from selenium.webdriver import ActionChains
import Levenshtein

from selenium.webdriver.common.by import By

from package.database import BetControl, LinksBetters


load_dotenv()

odds_pass = os.getenv('odds_pass')
odds_login = os.getenv('odds_login')


# <-- Helpers -->
def check_null_kw(keywords: list[list]) -> bool:
    if len(keywords) == 1:
        return True if keywords[0] else False
    return True

def jaccard_similarity(str1: str, str2: str) -> float:
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def levenshtein_similarity(str1: str, str2: str) -> float:
    distance = Levenshtein.distance(str1, str2)

    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    return (max_len - distance) / max_len

def check_command(str1: str, str2: str) -> bool:
    str1 = str1.lower().replace('(жен)', '').replace(' ', '')
    str2 = str2.lower().replace('(ж)', '').replace(' ', '')
    return True if (
            float(f"{levenshtein_similarity(str1, str2):.2f}") >= 0.67 or
            float(f"{jaccard_similarity(str1, str2):.2f}") >= 0.5
    ) else False


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def text_translator(text, src='en', dest='ru'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        if re.search(r"[a-zA-Z]", translation.text):
            sleep(uniform(1.5, 2.5))
            translation = translator.translate(text=text, src=src, dest=dest)

        return translation.text
    except Exception as ex:
        print('Translator err: ', ex)
        return text

def convert_date(date_str: str) -> str:
    current_year = 2024
    today = datetime.today()

    if "Today" in date_str:
        date_obj = today
        time_part = date_str.split(",")[1].strip()
    elif "Tomorr." in date_str:
        date_obj = today + timedelta(days=1)
        time_part = date_str.split(",")[1].strip()
    else:
        input_format = "%d/%b,%H:%M"
        date_obj = datetime.strptime(date_str, input_format)
        date_obj = date_obj.replace(year=current_year)
        time_part = date_obj.strftime("%H:%M")

    output_str = f"{time_part} {date_obj.strftime('%d.%m.%Y')}"
    return output_str
# <-- /Helpers -->


# <-- Pars helpers -->
def login_odds(driver: AntiDetectDriver, url: str) -> AntiDetectDriver:
    driver.get(url)
    driver.sleep(4)

    driver.click('div.loginModalBtn')
    driver.sleep(5)
    driver.find_element(By.CSS_SELECTOR, 'input#login-username-sign.int-text.border-box.border-black-main').send_keys(odds_login)
    driver.find_element(By.CSS_SELECTOR, 'input#login-password-sign-m.int-text.border-box.border-black-main').send_keys(odds_pass)
    driver.sleep(1)
    driver.click('input.font-secondary.text-black-main.orange-button-gradient')

    return driver


def check_predicts(driver: AntiDetectDriver):
    amount_predicted = driver.find_element(
        By.CLASS_NAME,
        'h-8.px-3.cursor-pointer.whitespace-nowrap.flex-center.bg-gray-medium.active-item-calendar'
    ).text
    try:
        return True if int(amount_predicted.split('(')[-1][:-1]) > 0 else False
    except ValueError:
        return False


def sort_and_transpose_lists(*lists):
    combined_lists = [list(tup) for tup in zip(*lists)]

    combined_lists.sort(key=lambda x: x[-1])

    transposed = list(zip(*combined_lists))
    transposed = [list(tup) for tup in transposed]

    return [list(tup) for tup in list(zip(*transposed))]


def get_pick_coefficient(card: BeautifulSoup) -> list:
    try:
        result = []
        X = [item.text for item in card.select(
            'div.border-black-borders.flex.min-h-\[30px\].min-w-\[60px\].items-center.justify-center.border-l')]
        coefficient = [item.text for item in card.select(
            'div.border-black-borders.flex.min-w-\[60px\].flex-col.items-center.justify-center.gap-1.border-l.pb-1.pt-1')]
        pick_x = dict(zip(X, coefficient))

        for k, v in pick_x.items():
            if 'PICK' in v:
                result.append(k)
                result.append(v.split('%')[0])
                break
        return result
    except:
        return []
    # pick = [int(item.text.replace('%', '')) for item in card.select(
    #     'div.border-black-main.min-sm\:min-h-\[26px\].min-sm\:min-w-\[80\%\].relative.flex.min-h-\[40px\].min-w-\[50px\].items-center.justify-start.border')]
    # return sort_and_transpose_lists(
    #     X,
    #     list(map(lambda item: float(item.replace('%', '')), coefficient)),
    #     pick
    # )[-1][:-1]


def check_correct_keywords(true_words: list[list], predicted_words: list[str], descr_ods_bet: str) -> bool:
    print(true_words, predicted_words, descr_ods_bet, sep=' --- ')
    flag = True
    for group in true_words:
        fl = True
        for keyword in group:
            if (keyword.lower() in [item.lower() for item in predicted_words]) or (keyword.lower() in descr_ods_bet.lower()):
                continue
            else:
                fl = False
                break

        if not fl:
            flag = False
        else:
            flag = True
            break
    return flag


def count_coef_by_formula(user_id: int, name: str, coef_portal: float) -> float:
    res_coef = float()
    _select = LinksBetters.select().where(LinksBetters.better_nickname == name, LinksBetters.user_id == user_id)
    if _select.exists():
        for item in _select:
            res_coef = (110 * coef_portal) / (100 + item.roi)
        return res_coef


def making_bet(bet: str, descr_ods_bet: str) -> str:
    if 'O/U' in descr_ods_bet:
        return 'тб' if bet == 'Over' else 'тм'
    elif '1X2' in descr_ods_bet or 'DC' in descr_ods_bet or 'H/A' in descr_ods_bet:
        return bet.lower()
    elif 'DNB' in descr_ods_bet:
        return 'ф1' if bet == '1' else 'ф2'
    elif 'BTS' in descr_ods_bet:
        return 'Обе забьют Нет' if bet.lower() == 'no' else 'Обе забьют Да'
    elif 'AH' in descr_ods_bet:
        if '-' in descr_ods_bet:
            return bet if bet.lower() == '1' else 'x2'
        elif '+' in descr_ods_bet:
            return '1x' if bet.lower() == '1' else '2'
    else:
        return 'stop'


def pars_predicts(driver: AntiDetectDriver, keywords: list[list], _user_id: int, bettor_name: str) -> list[dict]:
    result: list[dict] = list()
    driver.execute_script('window.scrollTo(0, 1666)')
    driver.sleep(1.1111)
    soup = driver.bs4()

    _main = soup.select_one('div.flex.w-full.flex-col.text-xs')
    all_pred_cards = _main.find_all('div', recursive=False)
    for card in all_pred_cards:
        try:
            if soup.select_one('p.text-red-dark.live-ping.whitespace-nowrap'):
                continue

            _pick: list = get_pick_coefficient(card=card)

            timeStart_ = convert_date(card.select_one('div.dropping-mt\:\!flex-row').text.replace(
                card.select_one('span.text-gray-dark').text, ''
            ))
            players_ = card.select_one('div.max-mt\:pl-1.flex.w-full.min-w-0.flex-col.gap-1').text
            sport_ = text_translator(card.select_one('div.flex').text.split('/')[0])
            if re.search(r"[a-zA-Z]", sport_):
                sport_ = text_translator(text=sport_)

            _select = BetControl.select().where(
                BetControl.scaner_name == "odds_portal",
                BetControl.timeStart == timeStart_,
                BetControl.players == players_,
                BetControl.sport == sport_
            )
            if _select.exists():
                continue
            if check_null_kw(keywords) and not check_correct_keywords(
                true_words=keywords,
                predicted_words=[item.lower().replace(" ", '') for item in card.select_one('div.flex').text.split('/')],
                descr_ods_bet=card.select_one('span.text-gray-dark').text
            ):
                continue
            res_bet = making_bet(_pick[0], card.select_one('span.text-gray-dark').text)
            if res_bet == 'stop':
                continue

            try:

                dct = {
                    'eg_or_rus': 'ruslan',
                    'scaner_name': 'odds_portal',
                    'bettors_name': bettor_name,
                    'timeStart': timeStart_,
                    'players': players_,
                    'bet': res_bet,
                    'coefficient': count_coef_by_formula(coef_portal=float(_pick[-1]), user_id=_user_id, name=bettor_name),  # !!!!!!!!!!!!!
                    'sport': sport_
                }
                BetControl.create(**dct)
            except Exception as ex:
                print(f'<-- DCT RESULT PARSER ERR: \n {ex}')
                continue
            result.append(dct)
        except Exception as ex:
            print(f'\n\n<-- EXEPTION not full card {ex}\n\n')

    print(f'\n<-- LEN MASS({bettor_name}) == {len(result)} -->\n')
    return result
# < /Pars helpers -->


# <-- Kush pars helpers -->
def check_sport(card, sport) -> bool:
    _sport_1 = card.find(
        'div', class_='d-block d-sm-inline-block mr-sm-2 mx-auto mx-sm-0 sportType sport1')
    _sport_2 = card.find(
        'div', class_='d-block d-sm-inline-block mr-sm-2 mx-auto mx-sm-0 sportType sport2')
    if _sport_1:
        if sport not in _sport_1.get('title') and _sport_1.get('title') not in sport:
            return False
    if _sport_2:
        if sport not in _sport_2.get('title') and _sport_2.get('title') not in sport:
            return False

    return True

def check_command_2(kush_cm, bet_cm) -> bool:
    cnt = 0

    kush_cm, new_kush = [i.lower() for i in kush_cm.rstrip().replace('.', ' ').split(' - ')], []

    for i in kush_cm:
        new_kush.extend(i.split(' '))
    bet_cm, new_bet = [i.lower() for i in bet_cm.rstrip().replace('.', ' ').split(' – ')], []
    for i in bet_cm:
        new_bet.extend(i.split(' '))

    for i in new_kush:
        if i in new_bet:
            cnt += 1
    for i in new_bet:
        if i in new_kush:
            cnt += 1

    if cnt > 2:
        return True
    return False


def check_date(odds: str, kush: str):
    # Преобразуем строку в объект datetime
    time_odds = datetime.strptime(odds, '%H:%M')
    time_kush = datetime.strptime(kush, '%H:%M')

    if time_odds.hour == time_kush.hour:
        return True

    if time_odds - timedelta(hours=1.5) <= time_kush <= time_odds + timedelta(hours=2.5):
        return True
    return False

def put_or_not(card: BeautifulSoup, date_odds, sport, bet_cm) -> bool:

    sport = text_translator(text=sport).capitalize()

    if re.search(r"[a-zA-Z]", sport):
        sleep(uniform(1, 4))
        sport = text_translator(text=sport)

    if not check_sport(card=card, sport=sport):
        return False

    data = card.select_one('a.notUnderlineHover').get('title')
    tm_and_dt = card.find('div', class_='d-block d-sm-inline-block time-event').text.replace('\n', '').split(' ')


    if tm_and_dt[-1] == 'Live' or 'назад' in tm_and_dt or 'Вчера' in tm_and_dt:
        return False

    if not check_date(odds=date_odds.split()[0], kush=tm_and_dt[-1]):
        return False

    _command = re.findall(
        r"[^\d]+", data)[0].rstrip().replace(
        'Прогнозы на матч ',
        ''
    )
    bet_cm = text_translator(text=bet_cm)
    if re.search(r"[a-zA-Z]", bet_cm):
        sleep(uniform(1, 4))
        bet_cm = text_translator(text=bet_cm)

    if not check_command(str1=_command, str2=bet_cm) and not check_command_2(kush_cm=_command, bet_cm=bet_cm):
        return False

    return True


def convert(bet: str, sport: str):
    # test_bet = bet.split("(")[0].split('/')[0].split('-')[0][0].lower().strip()  # проверка на 1(1:2) и 11-2
    #
    mass = ['Баскетбол']
    # if 'ничья' in bet.lower():
    #     return f"Основные#{bet.upper()}"
    # if (test_bet in ['1', '2', 'x'] and (len(bet) == 1 or len(test_bet) == 1)) or (bet.startswith('П')):
    #     bet = test_bet if len(bet) == 1 else bet[-1]
    if bet == '1' or bet == '2' or bet == 'x':
        return f"Основные#{bet.upper()}"

    if bet == 'тб' or bet == 'тм':
        return f'Тотал#{bet.upper()}'
    elif (bet == '1x' or bet == 'x2' or bet == '12') and sport not in mass:  # для всех, кроме баскета
        return f"Двойной исход#{bet.replace('x', '')}"
    elif bet == 'ф1' or bet == 'ф2':
        return f"Фора#{bet.upper()}"
    elif (bet == '1x' or bet == 'x2') and sport in mass:  # для баскета
        return f"Победа в матче#Победа в матче К{bet.replace('x', '')}"
    elif 'Обе забьют' in bet:
        return f"Обе забьют#{bet}"

def get_info(clear_bids, res) -> int:
    for idx in range(len(clear_bids)):
        if res == clear_bids[idx].text.rstrip():
            return idx


def make_bet(driver: AntiDetectDriver, data, dct, new_bet) -> bool:
    from uuid import uuid4
    cnt = 0.1
    while cnt < 7:
        for idx in range(len(data)):
            coefficient = dct['coefficient']
            bet, coefficient_kush = data[idx].text.split('\n')
            if new_bet.lower() in bet.lower() and float(coefficient) - 0.09 <= float(coefficient_kush) <= float(coefficient) + cnt:
                driver.sleep(uniform(1, 2))
                btn = data[idx].find_element(By.CSS_SELECTOR, 'a.coefLink.d-inline-block.px-0.px-sm-3.addCoupon')
                btn.click()
                driver.sleep(uniform(1, 2))
                btn2 = driver.find_element(By.ID, 'basketBetLine')
                btn2.click()
                driver.sleep(uniform(2, 3))

                slider = driver.find_element(By.XPATH, '//div[contains(@class, "slider-handle min-slider-handle round")]')
                move = ActionChains(driver)
                driver.sleep(uniform(2, 3))

                move.click_and_hold(slider).move_by_offset(-70, 0).release().perform()
                last_btn = driver.find_element(By.CSS_SELECTOR, 'button#add-bet-coupon.btn.btn-blue.w-100.mb-2')

                driver.sleep(3)
                driver.get_screenshot_as_file(f'all_screen/no_{uuid4}.png')

                last_btn.click()

                driver.sleep(3)
                driver.get_screenshot_as_file(f'all_screen/yes_{uuid4}.png')

                driver.sleep(3.1415926535)
                print('<--------  WIN  -------->\n\n\n')

                return True
        cnt += 0.08
    return False

# <-- /Kush pars helpers -->