"""Клиенты Wazzapo (синхронный) и AsyncWazzapo на httpx."""

from __future__ import annotations

import asyncio
import time
from typing import Any, AsyncIterator, Dict, Iterator, Mapping, Optional, Set

import httpx

from . import _http
from ._generated.attrs import AsyncResources, SyncResources
from ._generated.resources import RESOURCES


class _Base:
    _settings: _http.Settings

    @property
    def api_key_hint(self) -> str:
        """Ключ для логов: первые 8 знаков (wz_live_…). Сам ключ наружу не отдаётся."""
        return self._settings.key_hint

    @property
    def base_url(self) -> str:
        return self._settings.base_url

    @property
    def is_test(self) -> bool:
        """Ключ wz_test_: API ничего не отправляет и не меняет, ответы как настоящие."""
        return self._settings.is_test

    def __repr__(self) -> str:
        return f"{type(self).__name__}(api_key={self.api_key_hint!r}, base_url={self.base_url!r})"

    def _url(self, path: str) -> str:
        return self._settings.base_url + _http.API_PREFIX + path


class Wazzapo(_Base, SyncResources):
    """Клиент API v2.

    client = Wazzapo(api_key="wz_live_...")  # или переменная WAZZAPO_API_KEY
    client.messages.send(body={"phone_number_id": "...", "to": "77071234567", "type": "text", "text": {"body": "Привет"}})

    timeout: секунды на запрос (30), max_retries: повторы на 429, 5xx и сбоях сети (2).
    http_client: свой httpx.Client (прокси, свои заголовки); закрывать его будете вы.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._settings = _http.Settings.build(api_key, base_url, timeout, max_retries)
        self._own_http = http_client is None
        self._http = http_client or httpx.Client(timeout=self._settings.timeout)
        for name, (sync_cls, _async_cls) in RESOURCES.items():
            setattr(self, name, sync_cls(self))

    def close(self) -> None:
        if self._own_http:
            self._http.close()

    def __enter__(self) -> "Wazzapo":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        files: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_retries: Optional[int] = None,
        raw: bool = False,
    ) -> Any:
        request_headers = self._settings.headers(method, idempotency_key, headers)
        query = _http.clean_params(params)
        retries = self._settings.retries(max_retries)
        for attempt in range(retries + 1):
            last = attempt == retries
            _http.log_request(self._settings, method, path, attempt)
            try:
                response = self._http.request(
                    method,
                    self._url(path),
                    params=query,
                    json=json,
                    files=files,
                    headers=request_headers,
                    timeout=self._settings.timeout if timeout is None else timeout,
                )
            except httpx.TransportError as exc:
                if last:
                    raise _http.connection_error(exc) from exc
                time.sleep(_http.retry_delay(attempt, None))
                continue
            if not last and _http.should_retry(response):
                time.sleep(_http.retry_delay(attempt, response))
                continue
            return _http.result(response, raw)
        raise AssertionError("недостижимо")  # pragma: no cover

    def _paginate(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        *,
        timeout: Optional[float] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_retries: Optional[int] = None,
    ) -> Iterator[Any]:
        query = dict(params or {})
        seen: Set[str] = set()
        while True:
            page = self._request(
                "GET", path, params=query, timeout=timeout, headers=headers, max_retries=max_retries
            )
            yield from page.get("data") or []
            if _http.next_cursor(page, query, seen) is None:
                return


class AsyncWazzapo(_Base, AsyncResources):
    """Async-клиент API v2: те же методы, что у Wazzapo, через await.

    async with AsyncWazzapo() as client:
        await client.messages.send(body={...})
        async for contact in client.contacts.list_all():
            ...
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._settings = _http.Settings.build(api_key, base_url, timeout, max_retries)
        self._own_http = http_client is None
        self._http = http_client or httpx.AsyncClient(timeout=self._settings.timeout)
        for name, (_sync_cls, async_cls) in RESOURCES.items():
            setattr(self, name, async_cls(self))

    async def close(self) -> None:
        if self._own_http:
            await self._http.aclose()

    async def __aenter__(self) -> "AsyncWazzapo":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        files: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_retries: Optional[int] = None,
        raw: bool = False,
    ) -> Any:
        request_headers = self._settings.headers(method, idempotency_key, headers)
        query = _http.clean_params(params)
        retries = self._settings.retries(max_retries)
        for attempt in range(retries + 1):
            last = attempt == retries
            _http.log_request(self._settings, method, path, attempt)
            try:
                response = await self._http.request(
                    method,
                    self._url(path),
                    params=query,
                    json=json,
                    files=files,
                    headers=request_headers,
                    timeout=self._settings.timeout if timeout is None else timeout,
                )
            except httpx.TransportError as exc:
                if last:
                    raise _http.connection_error(exc) from exc
                await asyncio.sleep(_http.retry_delay(attempt, None))
                continue
            if not last and _http.should_retry(response):
                await asyncio.sleep(_http.retry_delay(attempt, response))
                continue
            return _http.result(response, raw)
        raise AssertionError("недостижимо")  # pragma: no cover

    async def _apaginate(
        self,
        path: str,
        params: Optional[Mapping[str, Any]] = None,
        *,
        timeout: Optional[float] = None,
        headers: Optional[Mapping[str, str]] = None,
        max_retries: Optional[int] = None,
    ) -> AsyncIterator[Any]:
        query = dict(params or {})
        seen: Set[str] = set()
        while True:
            page = await self._request(
                "GET", path, params=query, timeout=timeout, headers=headers, max_retries=max_retries
            )
            for item in page.get("data") or []:
                yield item
            if _http.next_cursor(page, query, seen) is None:
                return
