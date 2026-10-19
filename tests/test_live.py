"""Сквозной тест на тестовом ключе wz_test_: ничего не отправляет и не меняет.

Запуск: WAZZAPO_TEST_API_KEY=wz_test_... pytest tests/test_live.py
"""

from __future__ import annotations

import os

import pytest

import wazzapo

KEY = os.environ.get("WAZZAPO_TEST_API_KEY", "")
pytestmark = pytest.mark.skipif(not KEY.startswith("wz_test_"), reason="нет WAZZAPO_TEST_API_KEY с ключом wz_test_")


def test_sandbox_send_and_contact() -> None:
    with wazzapo.Wazzapo(api_key=KEY, base_url=os.environ.get("WAZZAPO_BASE_URL")) as client:
        assert client.is_test
        numbers = client.phone_numbers.list()["data"]
        assert isinstance(numbers, list)
        if numbers:
            sent = client.messages.send(
                body={
                    "phone_number_id": numbers[0]["phone_number_id"],
                    "to": "77074802540",
                    "type": "text",
                    "text": {"body": "Проверка SDK на тестовом ключе"},
                }
            )
            assert sent["message_id"].startswith("wamid.SANDBOX")
        contact = client.contacts.create(body={"phone": "77070000000", "name": "SDK test"})
        assert contact["id"]
