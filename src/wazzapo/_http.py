"""Общее для синхронного и async клиента: настройки, заголовки, повторы, разбор ответа."""

from __future__ import annotations

import logging
import os
import random
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional
from urllib.parse import quote

import httpx

from . import errors
from ._version import __version__

DEFAULT_BASE_URL = "https://wazzapo.kz"
API_PREFIX = "/api/v2/external"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
MAX_RETRY_AFTER = 60.0
TEST_KEY_PREFIX = "wz_test_"
USER_AGENT = f"wazzapo-sdk-python/{__version__}"

logger = logging.getLogger("wazzapo")


def _quote(value: str) -> str:
    """Параметр пути: id с / или пробелом не ломает адрес."""
    return quote(str(value), safe="")


def mask_key(key: str) -> str:
    """Ключ для логов и repr: первые 8 знаков, остальное скрыто."""
    return f"{key[:8]}…" if key else "<нет ключа>"


@dataclass(frozen=True)
class Settings:
    # repr=False: ключ не попадает ни в repr(settings), ни в отладочный вывод клиента
    api_key: str = field(repr=False)
    base_url: str
    timeout: float
    max_retries: int

    @classmethod
    def build(
        cls,
        api_key: Optional[str],
        base_url: Optional[str],
        timeout: Optional[float],
        max_retries: Optional[int],
    ) -> "Settings":
        key = api_key or os.environ.get("WAZZAPO_API_KEY") or ""
        if not key:
            raise errors.AuthenticationError(
                "Нет API-ключа: передайте api_key или задайте WAZZAPO_API_KEY "
                "(ключ в кабинете Wazzapo, раздел «API»)"
            )
        url = (base_url or os.environ.get("WAZZAPO_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        return cls(
            api_key=key,
            base_url=url,
            timeout=DEFAULT_TIMEOUT if timeout is None else timeout,
            max_retries=DEFAULT_MAX_RETRIES if max_retries is None else max_retries,
        )

    @property
    def is_test(self) -> bool:
        return self.api_key.startswith(TEST_KEY_PREFIX)

    @property
    def key_hint(self) -> str:
        return mask_key(self.api_key)

    def headers(
        self, method: str, idempotency_key: Optional[str], extra: Optional[Mapping[str, str]] = None
    ) -> Dict[str, str]:
        """Заголовки запроса; extra (свои заголовки вызова) не заменяют ключ и Idempotency-Key."""
        out = {"User-Agent": USER_AGENT, "Accept": "application/json", **dict(extra or {})}
        out["X-API-Key"] = self.api_key
        if method == "POST":
            out["Idempotency-Key"] = idempotency_key or uuid.uuid4().hex
        return out

    def retries(self, max_retries: Optional[int]) -> int:
        return self.max_retries if max_retries is None else max(max_retries, 0)


def clean_params(params: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    """Query без None; True и False как true и false."""
    if not params:
        return None
    out: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        out[key] = ("true" if value else "false") if isinstance(value, bool) else value
    return out or None


def retry_delay(attempt: int, response: Optional[httpx.Response]) -> float:
    """Пауза перед повтором: Retry-After из ответа или 0.5 × 2^n (не больше 8 с) ± 25 %."""
    wait = errors.parse_retry_after(response.headers.get("retry-after")) if response is not None else None
    if wait is not None:
        return min(wait, MAX_RETRY_AFTER)
    base = min(0.5 * (2.0**attempt), 8.0)
    return base * random.uniform(0.75, 1.25)


def should_retry(response: httpx.Response) -> bool:
    return response.status_code in RETRY_STATUSES


def parse_body(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def result(response: httpx.Response, raw: bool) -> Any:
    """Ответ 2xx → данные; иначе исключение из wazzapo.errors."""
    if response.is_success:
        if raw:
            return response.content
        if response.status_code == 204:
            return None
        return parse_body(response)
    raise errors.from_response(response.status_code, parse_body(response), response.headers)


def connection_error(exc: httpx.TransportError) -> errors.APIConnectionError:
    if isinstance(exc, httpx.TimeoutException):
        return errors.APITimeoutError(f"Сервер не ответил вовремя: {exc}", code=errors.TIMEOUT)
    return errors.APIConnectionError(f"Нет соединения с API: {exc}", code=errors.CONNECTION_ERROR)


def next_cursor(page: Any, query: Dict[str, Any], seen: set[str]) -> Optional[str]:
    """Курсор следующей страницы или None; тот же курсор второй раз → PaginationError."""
    if not isinstance(page, dict):
        return None
    cursor = page.get("next_cursor")
    if not page.get("has_more") or not cursor:
        return None
    if cursor in seen:
        raise errors.PaginationError(
            f"Сервер вернул тот же next_cursor ещё раз ({cursor}): обход остановлен", code="PAGINATION_LOOP"
        )
    seen.add(cursor)
    query["cursor"] = cursor
    return str(cursor)


def log_request(settings: Settings, method: str, path: str, attempt: int) -> None:
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "wazzapo %s %s попытка %d ключ %s", method, path, attempt + 1, mask_key(settings.api_key)
        )
