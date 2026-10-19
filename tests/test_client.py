"""Клиент на подставном HTTP: повторы, Idempotency-Key, ошибки, пагинация, 204, маскировка ключа."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List

import httpx
import pytest

import wazzapo
from wazzapo import errors
from wazzapo._http import USER_AGENT, retry_delay

KEY = "wz_live_0123456789abcdef"
SPEC = json.loads((Path(__file__).resolve().parent / "openapi.json").read_text(encoding="utf-8"))
SEND = {"phone_number_id": "123", "to": "77071234567", "type": "text", "text": {"body": "Привет"}}

Handler = Callable[[httpx.Request], httpx.Response]


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> List[float]:
    slept: List[float] = []

    async def fake_async_sleep(seconds: float) -> None:
        slept.append(seconds)

    monkeypatch.setattr("wazzapo._client.time.sleep", slept.append)
    monkeypatch.setattr("wazzapo._client.asyncio.sleep", fake_async_sleep)
    return slept


def client(handler: Handler, **kw: Any) -> wazzapo.Wazzapo:
    return wazzapo.Wazzapo(api_key=KEY, http_client=httpx.Client(transport=httpx.MockTransport(handler)), **kw)


def recorder(responses: List[httpx.Response]) -> tuple[List[httpx.Request], Handler]:
    seen: List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return responses[min(len(seen) - 1, len(responses) - 1)]

    return seen, handler


def test_send_builds_request() -> None:
    seen, handler = recorder([httpx.Response(200, json={"message_id": "wamid.1"})])
    out = client(handler).messages.send(body=SEND)
    req = seen[0]
    assert out == {"message_id": "wamid.1"}
    assert req.method == "POST" and str(req.url) == "https://wazzapo.kz/api/v2/external/messages/send"
    assert req.headers["X-API-Key"] == KEY and req.headers["User-Agent"] == USER_AGENT
    assert json.loads(req.content) == SEND
    assert len(req.headers["Idempotency-Key"]) == 32


def test_query_drops_none_and_formats_bool_and_quotes_path() -> None:
    seen, handler = recorder([httpx.Response(200, json={"data": [], "next_cursor": None, "has_more": False})])
    client(handler).conversations.list(unread=True, status=None, limit=10)
    assert seen[0].url.params == httpx.QueryParams({"unread": "true", "limit": "10"})
    seen2, handler2 = recorder([httpx.Response(200, json={"id": "a/b"})])
    client(handler2).contacts.get("a/b c")
    assert seen2[0].url.raw_path == b"/api/v2/external/contacts/a%2Fb%20c"


def test_retries_keep_one_idempotency_key_and_honor_retry_after(no_sleep: List[float]) -> None:
    seen, handler = recorder(
        [
            httpx.Response(429, headers={"Retry-After": "3"}, json={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "x"}}),
            httpx.Response(503, json={"error": {"code": "SERVICE_UNAVAILABLE", "message": "y"}}),
            httpx.Response(200, json={"message_id": "wamid.2"}),
        ]
    )
    out = client(handler).messages.send(body=SEND)
    assert out["message_id"] == "wamid.2" and len(seen) == 3
    assert len({r.headers["Idempotency-Key"] for r in seen}) == 1
    assert no_sleep[0] == 3.0 and 0.75 <= no_sleep[1] <= 1.25


def test_own_idempotency_key_is_sent() -> None:
    seen, handler = recorder([httpx.Response(201, json={"id": "c1"})])
    client(handler).contacts.create(body={"phone": "77071234567"}, idempotency_key="lead-42")
    assert seen[0].headers["Idempotency-Key"] == "lead-42"


def test_get_has_no_idempotency_key() -> None:
    seen, handler = recorder([httpx.Response(200, json={"data": []})])
    client(handler).phone_numbers.list()
    assert "Idempotency-Key" not in seen[0].headers


def test_retry_after_is_capped_and_backoff_grows() -> None:
    assert retry_delay(0, httpx.Response(429, headers={"Retry-After": "600"})) == 60.0
    assert retry_delay(0, httpx.Response(429, headers={"Retry-After": "soon"})) <= 0.625
    assert 6.0 <= retry_delay(10, None) <= 10.0


def test_gives_up_after_max_retries() -> None:
    seen, handler = recorder([httpx.Response(502, json={"error": {"code": "provider_error", "message": "Сбой Meta"}})])
    with pytest.raises(errors.ServerError) as info:
        client(handler, max_retries=1).messages.send(body=SEND)
    assert len(seen) == 2 and info.value.code == "provider_error"


def test_4xx_is_not_retried() -> None:
    seen, handler = recorder([httpx.Response(404, json={"error": {"code": "contact_not_found", "message": "нет"}})])
    with pytest.raises(errors.NotFoundError):
        client(handler).contacts.get("c1")
    assert len(seen) == 1


def test_network_error_is_retried_then_raised() -> None:
    calls: List[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        raise httpx.ConnectError("нет сети", request=request)

    with pytest.raises(errors.APIConnectionError):
        client(handler).phone_numbers.list()
    assert len(calls) == 3


def test_timeout_error_type() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("долго", request=request)

    with pytest.raises(errors.APITimeoutError):
        client(handler, max_retries=0).phone_numbers.list()
    assert errors.TimeoutError is errors.APITimeoutError


def _spec_error_examples() -> List[tuple[str, Dict[str, Any]]]:
    """Пример ответа каждого статуса ошибки из описания API (у всех методов одинаковые)."""
    responses = SPEC["paths"]["/api/v2/external/messages/send"]["post"]["responses"]
    return [(code, r["content"]["application/json"]["example"]) for code, r in sorted(responses.items()) if code[0] in "45"]


EXPECTED = {
    "400": errors.BadRequestError,
    "401": errors.AuthenticationError,
    "402": errors.PaymentRequiredError,
    "403": errors.PermissionDeniedError,
    "404": errors.NotFoundError,
    "409": errors.ConflictError,
    "422": errors.ValidationError,
    "429": errors.RateLimitError,
    "500": errors.ServerError,
    "501": errors.ServerError,
    "502": errors.ServerError,
    "503": errors.ServerError,
}


@pytest.mark.parametrize("status,example", _spec_error_examples())
def test_error_examples_from_spec(status: str, example: Dict[str, Any]) -> None:
    _, handler = recorder([httpx.Response(int(status), json=example, headers={"Retry-After": "0"})])
    with pytest.raises(errors.WazzapoError) as info:
        client(handler, max_retries=0).messages.send(body=SEND)
    err = info.value
    assert type(err) is EXPECTED[status]
    assert err.status == int(status) and err.code == example["error"]["code"]
    assert err.message == example["error"]["message"] and err.request_id == example["request_id"]
    assert err.details == example["error"].get("details")


@pytest.mark.parametrize(
    "status,code,cls",
    [
        (422, "outside_24h_window", errors.OutsideWindowError),
        (422, "template_paused", errors.TemplateError),
        (422, "invalid_parameters", errors.UnprocessableEntityError),
        (403, "USAGE_LIMIT_EXCEEDED", errors.UsageLimitError),
        (405, "METHOD_NOT_ALLOWED", errors.WazzapoError),
    ],
)
def test_error_class_by_code(status: int, code: str, cls: type) -> None:
    _, handler = recorder([httpx.Response(status, json={"success": False, "error": {"code": code, "message": "m"}})])
    with pytest.raises(errors.WazzapoError) as info:
        client(handler).messages.send(body=SEND)
    assert type(info.value) is cls
    assert isinstance(info.value, errors.UnprocessableEntityError) == (status == 422)


def test_rate_limit_retry_after_and_non_json_error() -> None:
    _, handler = recorder([httpx.Response(429, headers={"Retry-After": "7", "X-Request-Id": "r1"}, text="Too Many")])
    with pytest.raises(errors.RateLimitError) as info:
        client(handler, max_retries=0).phone_numbers.list()
    assert info.value.retry_after == 7.0 and info.value.message == "Too Many" and info.value.request_id == "r1"


def test_delete_returns_none_and_download_bytes() -> None:
    _, handler = recorder([httpx.Response(204)])
    assert client(handler).contacts.delete("c1") is None
    _, handler2 = recorder([httpx.Response(200, content=b"\x89PNG", headers={"Content-Type": "image/png"})])
    assert client(handler2).media.download("m1", phone_number_id="123") == b"\x89PNG"


def test_upload_sends_multipart(tmp_path: Path) -> None:
    file = tmp_path / "schet.pdf"
    file.write_bytes(b"%PDF-1.4")
    seen, handler = recorder([httpx.Response(200, json={"media_id": "m1"})])
    assert client(handler).media.upload(file, phone_number_id="123") == {"media_id": "m1"}
    req = seen[0]
    assert req.url.params["phone_number_id"] == "123"
    assert req.headers["Content-Type"].startswith("multipart/form-data")
    assert b'filename="schet.pdf"' in req.content and b"application/pdf" in req.content and b"%PDF-1.4" in req.content
    seen2, handler2 = recorder([httpx.Response(200, json={"media_id": "m2"})])
    client(handler2).media.upload(b"abc", filename="a.png", phone_number_id="123")
    assert b'filename="a.png"' in seen2[0].content and b"image/png" in seen2[0].content


def _pages() -> Handler:
    pages = {
        None: {"data": [{"id": "1"}, {"id": "2"}], "next_cursor": "c2", "has_more": True},
        "c2": {"data": [{"id": "3"}], "next_cursor": "c3", "has_more": True},
        "c3": {"data": [{"id": "4"}], "next_cursor": None, "has_more": False},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params.get("tag") == "vip"
        return httpx.Response(200, json=pages[request.url.params.get("cursor")])

    return handler


def test_list_all_walks_every_page() -> None:
    ids = [c["id"] for c in client(_pages()).contacts.list_all(tag="vip")]
    assert ids == ["1", "2", "3", "4"]


def test_one_page_and_cursor() -> None:
    page = client(_pages()).contacts.list(tag="vip", cursor="c2")
    assert page["next_cursor"] == "c3" and page["has_more"] is True


def test_key_is_masked(caplog: pytest.LogCaptureFixture) -> None:
    _, handler = recorder([httpx.Response(200, json={"data": []})])
    c = client(handler)
    assert KEY not in repr(c) and "wz_live_…" in repr(c)
    with caplog.at_level(logging.DEBUG, logger="wazzapo"):
        c.phone_numbers.list()
    assert caplog.records and all(KEY not in r.getMessage() for r in caplog.records)


def test_key_from_env_and_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WAZZAPO_API_KEY", "wz_test_fromenv")
    assert wazzapo.Wazzapo().is_test is True
    monkeypatch.delenv("WAZZAPO_API_KEY")
    with pytest.raises(errors.AuthenticationError):
        wazzapo.Wazzapo()


def test_every_resource_is_attached() -> None:
    c = wazzapo.Wazzapo(api_key=KEY)
    for name in ("messages", "phone_numbers", "templates", "media", "contacts", "deals", "tasks",
                 "pipelines", "conversations", "team", "webhooks", "webhook_event_types"):
        assert getattr(c, name)._client is c


async def test_async_client_retries_and_paginates() -> None:
    seen: List[httpx.Request] = []
    responses = [httpx.Response(500, json={"error": {"code": "INTERNAL_ERROR", "message": "x"}}), httpx.Response(200, json={"message_id": "w"})]

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return responses[len(seen) - 1]

    async with wazzapo.AsyncWazzapo(api_key=KEY, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as c:
        assert (await c.messages.send(body=SEND))["message_id"] == "w"
    assert len({r.headers["Idempotency-Key"] for r in seen}) == 1

    async with wazzapo.AsyncWazzapo(api_key=KEY, http_client=httpx.AsyncClient(transport=httpx.MockTransport(_pages()))) as c:
        ids = [x["id"] async for x in c.contacts.list_all(tag="vip")]
    assert ids == ["1", "2", "3", "4"]


async def test_async_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"error": {"code": "outside_24h_window", "message": "окно"}})

    async with wazzapo.AsyncWazzapo(api_key=KEY, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))) as c:
        with pytest.raises(errors.OutsideWindowError):
            await c.messages.send(body=SEND)
