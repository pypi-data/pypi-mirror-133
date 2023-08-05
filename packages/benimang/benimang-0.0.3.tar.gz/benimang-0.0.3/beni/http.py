import gzip
from http.client import HTTPResponse
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import (HTTPCookieProcessor, Request, build_opener,
                            install_opener, urlopen)

from beni import wrapper_retry, writefile_bytes
from beni.internal import makeHttpHeaders


@wrapper_retry(3)
def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 10):
    method = 'GET'
    headers = makeHttpHeaders(headers)
    request = Request(url=url, headers=headers or {}, method=method)
    response: HTTPResponse
    with urlopen(request, timeout=timeout) as response:
        result = response.read()
        if response.headers.get('Content-Encoding') == 'gzip':
            result = gzip.decompress(result)
        return result, response


@wrapper_retry(3)
def http_post(url: str, data: Any = None, headers: dict[str, str] | None = None, timeout: int = 10):
    method = 'POST'
    headers = makeHttpHeaders(headers)
    postData = data
    if type(data) is dict:
        postData = urlencode(data).encode()
    request = Request(url=url, data=postData, headers=headers, method=method)
    response: HTTPResponse
    with urlopen(request, timeout=timeout) as response:
        result = response.read()
        contentEncoding = response.headers.get('Content-Encoding')
        if contentEncoding == 'gzip':
            result = gzip.decompress(result)
        return result, response


def http_download(url: str, file: Path):
    result, _ = http_get(url)
    writefile_bytes(file, result)


# Cookie
_cookie = CookieJar()
_cookieProc = HTTPCookieProcessor(_cookie)
_opener = build_opener(_cookieProc)
install_opener(_opener)
