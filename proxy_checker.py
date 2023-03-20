import asyncio
import aiohttp
from datetime import datetime

from models import Proxy


async def check_proxy(proxy: Proxy):
    url = 'https://httpbin.org/get'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=f'http://{proxy.ip}:{proxy.port}', timeout=10) as resp:
                if resp.status == 200:
                    proxy.status = True
                else:
                    proxy.status = False
    except (aiohttp.ClientError, asyncio.TimeoutError):
        proxy.status = False
    proxy.last_checked = datetime.utcnow()
