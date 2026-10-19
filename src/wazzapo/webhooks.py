"""Проверка подписи вебхуков Wazzapo.

Каждый запрос на ваш адрес несёт заголовки:
    X-Wazzapo-Timestamp: unix-время отправки, секунды
    X-Wazzapo-Signature-V2: v2=<hex HMAC-SHA256(secret, timestamp + "." + тело)>
    X-Wazzapo-Delivery-Id: id доставки, один и тот же во всех повторах: по нему отсеивайте дубли

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
from typing import Iterable, Mapping, Optional, Protocol, Tuple, Union, cast

from ._generated.webhooks import EVENT_TYPES, WebhookEvent
from .errors import WebhookSignatureError, WebhookVerificationError

SIGNATURE_HEADER = "X-Wazzapo-Signature-V2"
TIMESTAMP_HEADER = "X-Wazzapo-Timestamp"
DELIVERY_ID_HEADER = "X-Wazzapo-Delivery-Id"
EVENT_HEADER = "X-Wazzapo-Event"
DEFAULT_TOLERANCE = 300
_PREFIX = "v2="


def _bytes(payload: Union[bytes, str]) -> bytes:
    return payload.encode("utf-8") if isinstance(payload, str) else payload


class HeadersLike(Protocol):
    """Любые заголовки с items(): dict, starlette Headers, werkzeug Headers (Flask)."""

    def items(self) -> Iterable[Tuple[str, str]]: ...


Headers = Union[Mapping[str, str], HeadersLike]


def _check_secret(secret: Optional[str]) -> str:
    # Пустой секрет: тело, подписанное пустым ключом, иначе прошло бы проверку
    if not isinstance(secret, str) or not secret:
        raise WebhookVerificationError(
            "Нет секрета вебхука: передайте секрет из webhooks.create или rotate_secret "
            "(часто это пустая переменная окружения)"
        )
    return secret


def compute_signature(payload: Union[bytes, str], secret: Optional[str], timestamp: int) -> str:
    """v2=<hex>: подпись тела с меткой времени."""
    secret = _check_secret(secret)
    mac = hmac.new(secret.encode("utf-8"), str(timestamp).encode() + b"." + _bytes(payload), hashlib.sha256)
    return _PREFIX + mac.hexdigest()


def sign(payload: Union[bytes, str], secret: Optional[str], timestamp: Optional[int] = None) -> dict[str, str]:
    """Заголовки, как их пришлёт Wazzapo: для своих тестов приёма вебхуков."""
    ts = int(time.time()) if timestamp is None else timestamp
    return {TIMESTAMP_HEADER: str(ts), SIGNATURE_HEADER: compute_signature(payload, secret, ts)}


def _header(headers: Headers, name: str) -> str:
    lower = name.lower()
    for key, value in headers.items():
        if key.lower() == lower:
            return value
    return ""


def verify(
    payload: Union[bytes, str],
    headers: Headers,
    secret: Optional[str],
    *,
    tolerance: int = DEFAULT_TOLERANCE,
    now: Optional[float] = None,
) -> WebhookEvent:
    """Проверяет подпись и время и возвращает событие.

    payload: тело запроса как пришло, до разбора JSON (иначе подпись не сойдётся)
    headers: заголовки запроса, регистр не важен (dict, request.headers во Flask, FastAPI, Django)
    secret: секрет вебхука; пустой или None сразу даёт ошибку
    tolerance: сколько секунд метка времени может отличаться от ваших часов (300)
    now: текущее unix-время для своих тестов, по умолчанию time.time()

    Ошибка WebhookVerificationError: нет секрета, подписи нет, она чужая, запрос старый или тело не JSON.
    """
    secret = _check_secret(secret)
    body = _bytes(payload)
    timestamp = _header(headers, TIMESTAMP_HEADER)
    signature = _header(headers, SIGNATURE_HEADER)
    if not timestamp.isdigit() or not signature:
        raise WebhookVerificationError(f"Нет заголовков {TIMESTAMP_HEADER} и {SIGNATURE_HEADER}")
    current = time.time() if now is None else now
    if abs(current - int(timestamp)) > tolerance:
        raise WebhookVerificationError("Метка времени вебхука старше допуска: запрос мог быть повторён злоумышленником")
    expected = compute_signature(body, secret, int(timestamp))
    candidates = [s.strip() for s in signature.split(",")]
    if not any(hmac.compare_digest(expected, s) for s in candidates):
        raise WebhookVerificationError("Подпись вебхука не сошлась: проверьте секрет")
    try:
        return cast(WebhookEvent, json.loads(body))
    except ValueError as exc:
        raise WebhookVerificationError("Тело вебхука не JSON, хотя подпись верна") from exc


__all__ = [
    "DEFAULT_TOLERANCE",
    "DELIVERY_ID_HEADER",
    "EVENT_HEADER",
    "EVENT_TYPES",
    "Headers",
    "SIGNATURE_HEADER",
    "TIMESTAMP_HEADER",
    "WebhookEvent",
    "WebhookSignatureError",
    "WebhookVerificationError",
    "compute_signature",
    "sign",
    "verify",
]
