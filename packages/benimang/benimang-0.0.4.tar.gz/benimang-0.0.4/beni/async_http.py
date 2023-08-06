from pathlib import Path
from typing import Any, Final
from urllib.parse import urlencode

import aiohttp

from beni.async_func import (set_async_limit, wrapper_async_limit,
                             wrapper_async_retry)
from beni.internal import makeHttpHeaders

LIMIT_TAG_HTTP: Final = 'http'

set_async_limit(LIMIT_TAG_HTTP, 50)


@wrapper_async_retry(3)
@wrapper_async_limit(LIMIT_TAG_HTTP)
async def async_http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 10):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=makeHttpHeaders(headers), timeout=timeout) as response:
            result = await response.read()
            return result, response


@wrapper_async_retry(3)
@wrapper_async_limit(LIMIT_TAG_HTTP)
async def async_http_post(url: str, data: Any = None, headers: dict[str, str] | None = None, timeout: int = 10):
    headers = makeHttpHeaders(headers)
    postData = data
    if type(data) is dict:
        postData = urlencode(data).encode()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=postData, headers=headers, timeout=timeout) as response:
            result = await response.read()
            return result, response


async def async_http_download(url: str, file: Path):
    result, _ = await async_http_get(url)
    import async_file
    await async_file.async_writefile_bytes(file, result)
