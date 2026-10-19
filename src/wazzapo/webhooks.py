"""Проверка подписи вебхуков Wazzapo.

Каждый запрос на ваш адрес несёт заголовки:
    X-Wazzapo-Timestamp: unix-время отправки, секунды
    X-Wazzapo-Signature-V2: v2=<hex HMAC-SHA256(secret, timestamp + "." + тело)>

Секрет выдаётся один раз при создании вебхука (webhooks.create) и при rotate_secret.

    from wazzapo import webhooks
    event = webhooks.verify(request_body_bytes, request.headers, secret)
    if event["event"] == "message.incoming":
        ...
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Mapping, Optional, Union, cast

from ._generated.webhooks import EVENT_TYPES, WebhookEvent
from .errors import WebhookSignatureError

SIGNATURE_HEADER = "X-Wazzapo-Signature-V2"
TIMESTAMP_HEADER = "X-Wazzapo-Timestamp"
DEFAULT_TOLERANCE = 300
_PREFIX = "v2="


def _bytes(payload: Union[bytes, str]) -> bytes:
    return payload.encode("utf-8") if isinstance(payload, str) else payload


def compute_signature(payload: Union[bytes, str], secret: str, timestamp: int) -> str:
    """v2=<hex>: подпись тела с меткой времени."""
    mac = hmac.new(secret.encode("utf-8"), str(timestamp).encode() + b"." + _bytes(payload), hashlib.sha256)
    return _PREFIX + mac.hexdigest()


def sign(payload: Union[bytes, str], secret: str, timestamp: Optional[int] = None) -> dict[str, str]:
    """Заголовки, как их пришлёт Wazzapo: для своих тестов приёма вебхуков."""
    ts = int(time.time()) if timestamp is None else timestamp
    return {TIMESTAMP_HEADER: str(ts), SIGNATURE_HEADER: compute_signature(payload, secret, ts)}


def _header(headers: Mapping[str, str], name: str) -> str:
    lower = name.lower()
    for key, value in headers.items():
        if key.lower() == lower:
            return value
    return ""


def verify(
    payload: Union[bytes, str],
    headers: Mapping[str, str],
    secret: str,
    *,
    tolerance: int = DEFAULT_TOLERANCE,
) -> WebhookEvent:
    """Проверяет подпись и время и возвращает событие.

    payload: тело запроса как пришло, до разбора JSON (иначе подпись не сойдётся)
    headers: заголовки запроса, регистр не важен
    tolerance: сколько секунд метка времени может отличаться от ваших часов (300)

    Ошибка WebhookSignatureError: подписи нет, она чужая или запрос старый.
    """
    body = _bytes(payload)
    timestamp = _header(headers, TIMESTAMP_HEADER)
    signature = _header(headers, SIGNATURE_HEADER)
    if not timestamp.isdigit() or not signature:
        raise WebhookSignatureError(f"Нет заголовков {TIMESTAMP_HEADER} и {SIGNATURE_HEADER}")
    if abs(time.time() - int(timestamp)) > tolerance:
        raise WebhookSignatureError("Метка времени вебхука старше допуска: запрос мог быть повторён злоумышленником")
    expected = compute_signature(body, secret, int(timestamp))
    candidates = [s.strip() for s in signature.split(",")]
    if not any(hmac.compare_digest(expected, s) for s in candidates):
        raise WebhookSignatureError("Подпись вебхука не сошлась: проверьте секрет")
    return cast(WebhookEvent, json.loads(body))


__all__ = [
    "DEFAULT_TOLERANCE",
    "EVENT_TYPES",
    "SIGNATURE_HEADER",
    "TIMESTAMP_HEADER",
    "WebhookEvent",
    "WebhookSignatureError",
    "compute_signature",
    "sign",
    "verify",
]
