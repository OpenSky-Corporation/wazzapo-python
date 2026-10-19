"""Подпись вебхука: как её ставит backend (v2=HMAC-SHA256(secret, "timestamp.body"))."""

from __future__ import annotations

import hashlib
import hmac
import json
import time

import pytest

from wazzapo import webhooks
from wazzapo.errors import WebhookSignatureError

SECRET = "whsec_test"
BODY = json.dumps({"event": "test", "timestamp": "2026-10-19T09:00:00Z", "data": {}}).encode()


def backend_headers(body: bytes, secret: str, ts: int) -> dict:
    """Так подписывает backend/app/services/webhook_delivery_service.py (_sign_v2)."""
    mac = hmac.new(secret.encode(), str(ts).encode() + b"." + body, hashlib.sha256)
    return {"x-wazzapo-timestamp": str(ts), "X-WAZZAPO-SIGNATURE-V2": f"v2={mac.hexdigest()}"}


def test_valid_signature_returns_event() -> None:
    event = webhooks.verify(BODY, backend_headers(BODY, SECRET, int(time.time())), SECRET)
    assert event["event"] == "test"


def test_str_body_and_sign_roundtrip() -> None:
    headers = webhooks.sign(BODY.decode(), SECRET)
    assert webhooks.verify(BODY.decode(), headers, SECRET)["event"] == "test"


def test_wrong_secret_rejected() -> None:
    with pytest.raises(WebhookSignatureError, match="не сошлась"):
        webhooks.verify(BODY, backend_headers(BODY, "чужой", int(time.time())), SECRET)


def test_tampered_body_rejected() -> None:
    headers = backend_headers(BODY, SECRET, int(time.time()))
    with pytest.raises(WebhookSignatureError):
        webhooks.verify(BODY.replace(b"test", b"tost"), headers, SECRET)


def test_old_timestamp_rejected() -> None:
    old = int(time.time()) - 301
    with pytest.raises(WebhookSignatureError, match="старше"):
        webhooks.verify(BODY, backend_headers(BODY, SECRET, old), SECRET)
    assert webhooks.verify(BODY, backend_headers(BODY, SECRET, old), SECRET, tolerance=600)["event"] == "test"


def test_missing_headers_rejected() -> None:
    with pytest.raises(WebhookSignatureError, match="Нет заголовков"):
        webhooks.verify(BODY, {}, SECRET)


def test_event_types_cover_spec() -> None:
    assert {"message.incoming", "message.status", "deal.created", "test"} <= set(webhooks.EVENT_TYPES)
