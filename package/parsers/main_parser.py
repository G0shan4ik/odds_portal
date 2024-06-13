import asyncio
from ast import literal_eval
from typing import Awaitable

from botasaurus import browser, bt

from .helpers import *
from package.database import LinksBetters
from .kush_parser import get_result


@browser(
    user_agent=bt.UserAgent.user_agent_106,
    reuse_driver=True,
    headless=True,
    add_arguments=['--disable-dev-shm-usage', '--no-sandbox', '--disable-gpu']
)
def pars_odds(driver: AntiDetectDriver, data: str) -> list[dict]:
    url, keywords, _user_id, bettor_name = data.split('#')

    # <-- LOGIN TO PORTAL -->
    login_odds(driver=driver, url=url)
    driver.sleep(round(uniform(1.5, 3.5), 3))
    # <-- /LOGIN TO PORTAL -->

    # <-- CHECK PREDICTS -->
    if not check_predicts(driver=driver):
        return []
    # <-- /CHECK PREDICTS -->

    # <-- PARS RESULT  -->
    return pars_predicts(driver=driver, keywords=literal_eval(keywords), _user_id=_user_id, bettor_name=bettor_name)
    # <-- /PARS RESULT  -->


async def pars_manager(item: LinksBetters, user_id: int, loop: asyncio.AbstractEventLoop):
    url = f'{item.link}#{item.keyword.split(" | ")}#{user_id}#{item.better_nickname}'
    data: list[dict] = await loop.run_in_executor(None, pars_odds, url)
    await asyncio.sleep(1)
    if data:
        await get_result(loop=loop, forks=data)


async def schedule():
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    while True:
        try:
            await asyncio.sleep(1)
            _select: list[LinksBetters] = LinksBetters.select()
            processes: [Awaitable] = []

            for item in _select:
                if item.roi > 2 and item.on_off:
                    user_id = item.user_id
                    processes.append(pars_manager(item=item, user_id=user_id, loop=loop))

            for items in chunks(processes, 5):
                await asyncio.gather(*items)

            await asyncio.sleep(60)
        except Exception as ex:
            print(f"<-- Schedule err: {ex} -->")
            await asyncio.sleep(360)
