import asyncio
from functools import partial
from typing import Optional, Any

import requests
from requests import *


async def run_sync_func(func, *args, **kwargs) -> Any:
    return await asyncio.get_event_loop().run_in_executor(
        None, partial(func, *args, **kwargs))

_global_session = Session()

class AsyncResponse:
    def __init__(self, response: requests.Response):
        self.raw_response = response
        self._closed = False

    def close(self):
        if self._closed:
            return
        self.raw_response.close()
        self._closed = True

    def __del__(self):
        self.close()

    @property
    def ok(self) -> bool:
        return self.raw_response.ok
    
    @property
    def status_code(self) -> int:
        return self.raw_response.status_code
    
    @property
    def headers(self):
        return self.raw_response.headers
    
    @property
    def url(self):
        return self.raw_response.url
    
    @property
    def encoding(self):
        return self.raw_response.encoding
    
    @property
    def cookies(self):
        return self.raw_response.cookies

    def __repr__(self):
        return '<AsyncResponse [%s]>' % self.raw_response.status_code

    def __bool__(self):
        return self.ok

    @property
    async def content(self) -> Optional[bytes]:
        try:
            return await run_sync_func(lambda: self.raw_response.content)
        finally:
            self.close()

    @property
    async def text(self) -> str:
        try:
            return await run_sync_func(lambda: self.raw_response.text)
        finally:
            self.close()

    async def json(self, **kwargs) -> Any:
        try:
            return await run_sync_func(self.raw_response.json, **kwargs)
        finally:
            self.close()
    
    def raise_for_status(self):
        try:
            self.raw_response.raise_for_status()
        except Exception:
            self.close()
            raise


async def request(method, url, **kwargs) -> AsyncResponse:
    return AsyncResponse(await run_sync_func(_global_session.request,
                                             method=method, url=url, **kwargs))


async def get(url, params=None, **kwargs) -> AsyncResponse:
    return AsyncResponse(
        await run_sync_func(_global_session.get, url=url, params=params, **kwargs))


async def options(url, **kwargs) -> AsyncResponse:
    return AsyncResponse(
        await run_sync_func(_global_session.options, url=url, **kwargs))


async def head(url, **kwargs) -> AsyncResponse:
    return AsyncResponse(await run_sync_func(_global_session.head, url=url, **kwargs))


async def post(url, data=None, json=None, **kwargs) -> AsyncResponse:
    return AsyncResponse(await run_sync_func(_global_session.post, url=url,
                                             data=data, json=json, **kwargs))


async def put(url, data=None, **kwargs) -> AsyncResponse:
    return AsyncResponse(
        await run_sync_func(_global_session.put, url=url, data=data, **kwargs))


async def patch(url, data=None, **kwargs) -> AsyncResponse:
    return AsyncResponse(
        await run_sync_func(_global_session.patch, url=url, data=data, **kwargs))


async def delete(url, **kwargs) -> AsyncResponse:
    return AsyncResponse(
        await run_sync_func(_global_session.delete, url=url, **kwargs))
