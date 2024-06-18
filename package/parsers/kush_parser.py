import asyncio
from ast import literal_eval
from typing import Awaitable

from botasaurus import *

from .helpers import *
from package.database import *

from dotenv import load_dotenv
import os


load_dotenv()


LOGIN_KUSH_RUSLAN = os.getenv('LOGIN_KUSH_RUSLAN')
PASS_KUSH_RUSLAN = os.getenv('PASS_KUSH_RUSLAN')
PROXY_RUSLAN = os.getenv('PROXY_RUSLAN')


# LOGIN_KUSH_EGOR = os.getenv('LOGIN_KUSH_EGOR')
# PASS_KUSH_EGOR = os.getenv('PASS_KUSH_EGOR')
# PROXY_EGOR = os.getenv('PROXY_EGOR')


def get_start_url(data):
    return data


@browser(
    user_agent=bt.UserAgent.user_agent_106,
    proxy=PROXY_RUSLAN,
    headless=True,
    add_arguments=['--disable-dev-shm-usage', '--no-sandbox', '--disable-gpu']
)
def submit_and_pars_kush(driver: AntiDetectDriver, data: str) -> bool:
    try:
        data = data.split('#')

        dct = literal_eval(data[1])
        print(dct)
        driver.get(data[0])
        driver.sleep(1)

        # <-- sign in kush -->
        loginButton = driver.find_element('id', 'authModalButton')
        loginButton.click()

        driver.sleep(uniform(1, 2))

        loginField = driver.find_element('name', 'login-form[login]')
        loginField.send_keys(data[2])
        passwordField = driver.find_element('name', 'login-form[password]')
        passwordField.send_keys(data[3])
        loginButton = driver.find_element(By.XPATH, '//button[contains(@class, "btn btn-blue")]')
        loginButton.click()
        driver.sleep(uniform(4, 7))
        # <-- /sign in kush -->
        driver.execute_script('window.scrollTo(0, 1666)')
        driver.sleep(uniform(2, 4))
        try:
            soup: BeautifulSoup = driver.bs4()

            all_cards = soup.select_one('div[id="list-events"]').select('div.event-block.border-block.mb-3')
        except:
            driver.sleep(6)
            soup: BeautifulSoup = driver.bs4()
            all_cards = soup.select_one('div[id="list-events"]').select('div.event-block.border-block.mb-3')
        flag = False
        cnt = 0
        for card in all_cards:
            cnt += 1
            if put_or_not(card=card, date=dct['timeStart'], sport=dct['sport'], bet_cm=dct['players']):
                flag = True
                link = card.select_one('a.addBetsButton').get('href')
                driver.get(f"https://kushvsporte.ru{link}")
                driver.sleep(uniform(1, 2))
                break
            elif cnt > 7:
                break

        if not flag:
            print('\nflag -> False')
            print(dct['players'], '\n')
            return False

        driver.execute_script('window.scrollTo(0, 808)')
        driver.sleep(uniform(2, 4))
        try:
            driver.sleep(uniform(5, 7))
            driver.find_element(
                By.CSS_SELECTOR,
                'a.w-100.mb-3.load-cf-list.greenButton.d-block.greenBackground.text-center.white').click()
        except:
            driver.sleep(14)
            driver.find_element(
                By.CSS_SELECTOR,
                'a.w-100.mb-3.load-cf-list.greenButton.d-block.greenBackground.text-center.white').click()
        try:
            driver.sleep(uniform(7, 10))
            result, new_bet = convert(bet=dct['bet'], sport=dct['sport']).split('#')
        except:
            driver.sleep(13)
            result, new_bet = convert(bet=dct['bet'], sport=dct['sport']).split('#')

        try:
            driver.sleep(uniform(3, 5))
            sp = driver.bs4()
            clear_bids = sp.select_one('div.coefBlock').select('a[data-toggle="collapse"]')
            num = get_info(clear_bids, res=result)
        except:
            driver.sleep(uniform(6, 10))
            sp = driver.bs4()
            clear_bids = sp.find('div', class_='coefBlock').select('a[data-toggle="collapse"]')
            num = get_info(clear_bids, res=result)

        bid = driver.find_element(
            By.CSS_SELECTOR,
            'div.coefBlock'
        ).find_elements(By.CSS_SELECTOR, 'a[data-toggle="collapse"]')[num]
        bid.click()
        try:
            driver.sleep(uniform(4, 7))

            data = driver.find_elements(
                By.CSS_SELECTOR,
                'div.collapse.show'
            )[1].find_elements(By.CSS_SELECTOR, 'div.d-flex.justify-content-between.align-items-center')
        except Exception as ex:
            print(ex)
            driver.sleep(13)
            data = driver.find_elements(
                By.CSS_SELECTOR,
                'div.collapse.show'
            )[1].find_elements(By.CSS_SELECTOR, 'div.d-flex.justify-content-between.align-items-center')

        return make_bet(driver=driver, data=data, dct=dct, new_bet=new_bet)

    except Exception as ex:
        print(ex)
        return False


async def kush_get_result(url: str, loop: asyncio.AbstractEventLoop, proxy: str):
    # def foo():
    #     asyncio.create_task(submit_and_pars_kush(data=url, proxy=proxy))

    await loop.run_in_executor(None, submit_and_pars_kush, url)


async def get_result(loop: asyncio.AbstractEventLoop, forks: list[dict]) -> None:
    res_mass: list[Awaitable] = []

    if forks:
        for fork in forks:

            # login_kush = LOGIN_KUSH_RUSLAN
            # pass_kush = PASS_KUSH_RUSLAN
            # proxy_kush = PROXY_RUSLAN
            # if fork['eg_or_rus'] == 'егор':
            login_kush = LOGIN_KUSH_RUSLAN
            pass_kush = PASS_KUSH_RUSLAN
            proxy_kush = PROXY_RUSLAN

            if isinstance(fork, dict):
                player = text_translator(text=fork["players"]).capitalize()
                if re.search(r"[a-zA-Z]", player):
                    await asyncio.sleep(uniform(1, 4))
                    player = text_translator(text=player)
                fork["players"] = player
                url = f'https://kushvsporte.ru/site/search?q={player}#{fork}#{login_kush}#{pass_kush}'
                await asyncio.sleep(uniform(1, 2))
                res_mass.append(kush_get_result(url=url, loop=loop, proxy=proxy_kush))

    if res_mass:
        for i in chunks(res_mass, 2):
            await asyncio.gather(*i)

    return None