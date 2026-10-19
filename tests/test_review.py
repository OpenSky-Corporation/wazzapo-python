"""Исправления после проверки 19.10.2026 (docs/api/SDK.md, «Сверка языков»)."""

from __future__ import annotations

import json
import time
from email.utils import format_datetime
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, List

import httpx
import pytest

import wazzapo
from wazzapo import errors, webhooks
from wazzapo._http import retry_delay

from .test_client import KEY, SEND, client, recorder

SECRET = "whsec_test"
BODY = json.dumps({"event": "test", "timestamp": "2026-10-19T09:00:00Z", "data": {}}).encode()


# ─── Вебхуки ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("secret", ["", None])
def test_empty_secret_is_rejected_even_for_body_signed_with_empty_key(secret: Any) -> None:
    import hashlib
    import hmac

    ts = int(time.time())
    forged = "v2=" + hmac.new(b"", str(ts).encode() + b"." + BODY, hashlib.sha256).hexdigest()
    headers = {webhooks.TIMESTAMP_HEADER: str(ts), webhooks.SIGNATURE_HEADER: forged}
    with pytest.raises(errors.WebhookVerificationError, match="Нет секрета"):
        webhooks.verify(BODY, headers, secret)
    with pytest.raises(errors.WebhookVerificationError):
        webhooks.sign(BODY, secret)


def test_verification_error_hierarchy_and_old_name() -> None:
    assert issubclass(errors.WebhookVerificationError, errors.WazzapoError)
    assert issubclass(errors.WebhookVerificationError, ValueError)
    assert errors.WebhookSignatureError is errors.WebhookVerificationError
    assert wazzapo.WebhookVerificationError is errors.WebhookVerificationError


def test_non_json_body_with_valid_signature() -> None:
    body = b"not json"
    with pytest.raises(errors.WebhookVerificationError, match="не JSON"):
        webhooks.verify(body, webhooks.sign(body, SECRET), SECRET)


def test_verify_now_for_tests() -> None:
    headers = webhooks.sign(BODY, SECRET, timestamp=1_000_000)
    assert webhooks.verify(BODY, headers, SECRET, now=1_000_100)["event"] == "test"
    with pytest.raises(errors.WebhookVerificationError, match="Метка времени"):
        webhooks.verify(BODY, headers, SECRET, now=1_000_000 + 301)


def test_one_of_several_signatures_is_enough() -> None:
    headers = webhooks.sign(BODY, SECRET)
    headers[webhooks.SIGNATURE_HEADER] = "v2=" + "0" * 64 + ", " + headers[webhooks.SIGNATURE_HEADER]
    assert webhooks.verify(BODY, headers, SECRET)["event"] == "test"


def test_headers_object_with_items_only() -> None:
    class FlaskLikeHeaders:
        def __init__(self, pairs: List[tuple[str, str]]) -> None:
            self._pairs = pairs

        def items(self) -> List[tuple[str, str]]:
            return self._pairs

    headers = FlaskLikeHeaders(list(webhooks.sign(BODY, SECRET).items()))
    assert webhooks.verify(BODY, headers, SECRET)["event"] == "test"


def test_delivery_id_header_constant() -> None:
    assert webhooks.DELIVERY_ID_HEADER == "X-Wazzapo-Delivery-Id"


# ─── Ключ ───────────────────────────────────────────────────────────────────


def test_key_hidden_in_settings_repr_and_vars() -> None:
    c = wazzapo.Wazzapo(api_key=KEY)
    assert KEY not in repr(c._settings)
    assert KEY not in repr(vars(c))
    assert c.api_key_hint == "wz_live_…"
    assert not hasattr(c, "api_key")


def test_missing_key_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WAZZAPO_API_KEY", raising=False)
    with pytest.raises(errors.AuthenticationError, match="Нет API-ключа: передайте api_key или задайте WAZZAPO_API_KEY"):
        wazzapo.Wazzapo()


# ─── Вызовы ─────────────────────────────────────────────────────────────────


def test_body_positional_and_keyword() -> None:
    seen, handler = recorder([httpx.Response(200, json={"message_id": "wamid.1"})])
    c = client(handler)
    c.messages.send(SEND)
    c.messages.send(body=SEND)
    c.contacts.update("c1", {"name": "Айгуль"})
    assert json.loads(seen[0].content) == json.loads(seen[1].content) == SEND
    assert json.loads(seen[2].content) == {"name": "Айгуль"} and seen[2].url.path.endswith("/contacts/c1")


def test_per_call_headers_and_max_retries() -> None:
    seen, handler = recorder([httpx.Response(503)])
    c = client(handler)
    with pytest.raises(errors.ServerError):
        c.messages.send(SEND, headers={"X-Request-Id": "my-1", "X-API-Key": "чужой"}, max_retries=0)
    assert len(seen) == 1
    assert seen[0].headers["X-Request-Id"] == "my-1" and seen[0].headers["X-API-Key"] == KEY


def test_upload_missing_file_fails_before_request(tmp_path: Path) -> None:
    seen, handler = recorder([httpx.Response(200, json={"media_id": "m1"})])
    with pytest.raises(FileNotFoundError, match="не найден"):
        client(handler).media.upload(tmp_path / "nope.pdf", phone_number_id="123")
    assert seen == []


# ─── Ошибки ─────────────────────────────────────────────────────────────────


def test_validation_error_fields() -> None:
    body = {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Request validation failed",
                                        "details": [{"field": "body.to", "message": "Field required"}]}}
    _, handler = recorder([httpx.Response(422, json=body)])
    with pytest.raises(errors.ValidationError) as info:
        client(handler).messages.send(SEND)
    assert isinstance(info.value, errors.UnprocessableEntityError)
    assert info.value.fields == [{"field": "body.to", "message": "Field required"}]


def test_bad_request_class() -> None:
    _, handler = recorder([httpx.Response(400, json={"success": False, "error": {"code": "BAD_REQUEST", "message": "x"}})])
    with pytest.raises(errors.BadRequestError):
        client(handler).messages.send(SEND)


@pytest.mark.parametrize("status,code", [(502, "BAD_GATEWAY"), (404, "NOT_FOUND"), (504, "GATEWAY_TIMEOUT")])
def test_non_api_response_gets_code_by_status(status: int, code: str) -> None:
    _, handler = recorder([httpx.Response(status, text="<html>nginx</html>")])
    with pytest.raises(errors.WazzapoError) as info:
        client(handler, max_retries=0).phone_numbers.list()
    assert info.value.code == code


def test_connection_and_timeout_codes() -> None:
    def refused(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused")

    def slow(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow")

    with pytest.raises(errors.APIConnectionError) as info:
        client(refused, max_retries=0).phone_numbers.list()
    assert info.value.code == "CONNECTION_ERROR"
    with pytest.raises(errors.APITimeoutError) as info2:
        client(slow, max_retries=0).phone_numbers.list()
    assert info2.value.code == "TIMEOUT"


def test_builtin_names_not_shadowed_by_star_import() -> None:
    namespace: dict = {}
    exec("from wazzapo.errors import *", namespace)
    assert "ConnectionError" not in namespace and "TimeoutError" not in namespace
    assert errors.ConnectionError is errors.APIConnectionError  # синоним остаётся атрибутом


# ─── Повторы и списки ───────────────────────────────────────────────────────


def test_retry_after_http_date() -> None:
    when = datetime.now(timezone.utc) + timedelta(seconds=20)
    delay = retry_delay(0, httpx.Response(429, headers={"Retry-After": format_datetime(when, usegmt=True)}))
    assert 15 <= delay <= 21
    past = format_datetime(datetime.now(timezone.utc) - timedelta(hours=1), usegmt=True)
    assert retry_delay(0, httpx.Response(429, headers={"Retry-After": past})) == 0.0
    err = errors.from_response(429, None, {"Retry-After": format_datetime(when, usegmt=True)})
    assert isinstance(err, errors.RateLimitError) and err.retry_after is not None and 15 <= err.retry_after <= 21


def test_repeated_cursor_stops_with_error() -> None:
    page = {"data": [{"id": "1"}], "next_cursor": "same", "has_more": True}
    seen, handler = recorder([httpx.Response(200, json=page)])
    with pytest.raises(errors.PaginationError):
        list(client(handler).contacts.list_all())
    assert len(seen) == 2


async def test_async_repeated_cursor_stops() -> None:
    page = {"data": [{"id": "1"}], "next_cursor": "same", "has_more": True}
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json=page))
    c = wazzapo.AsyncWazzapo(api_key=KEY, http_client=httpx.AsyncClient(transport=transport))
    with pytest.raises(errors.PaginationError):
        async for _ in c.contacts.list_all():
            pass
