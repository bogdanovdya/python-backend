import requests
from time import time
import asyncio

SITES = ['www.google.com', 'www.yandex.ru', 'www.lenta.ru', 'www.rbc.ru', 'rg.ru']


async def get_sites(site):
    r = await requests.get("https://" + site)
    r.status_code


async def async_foo():
    t0 = time()
    tasks = [asyncio.ensure_future(get_sites(site)) for i in SITES]
    await asyncio.wait(tasks)
    t1 = time()
    return t1 - t0


print(async_foo())