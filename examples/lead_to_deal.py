"""Заявка с сайта в сделку: форма шлёт POST name, phone, comment, пример создаёт сделку
и отправляет клиенту приветственный шаблон WhatsApp.

Запуск: WAZZAPO_API_KEY=... WAZZAPO_PHONE_NUMBER_ID=... WAZZAPO_TEMPLATE_NAME=... python lead_to_deal.py
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qsl

from wazzapo import Wazzapo
from wazzapo.errors import ConflictError, WazzapoError
from wazzapo.types import TemplateMessageIn

client = Wazzapo()


def env(name: str, default: str = "") -> str:
    return os.environ.get(name) or default


def deal_for(lead: dict[str, str]) -> tuple[Any, bool]:
    """Сделка без дублей: повтор той же заявки (двойной клик, перезагрузка страницы) вернёт уже созданную."""
    pipeline_id = env("WAZZAPO_PIPELINE_ID") or client.pipelines.list()["data"][0]["id"]
    # Свой id заявки из формы или CRM; без него считаем по телефону и тексту, чтобы повтор совпал
    external_id = lead["lead_id"] or "site-" + hashlib.sha1(f"{lead['phone']}|{lead['comment']}".encode()).hexdigest()
    try:
        deal = client.deals.create({
            "pipeline_id": pipeline_id,
            "title": "Заявка с сайта: " + (lead["name"] or lead["phone"]),
            # Контакт по телефону: Wazzapo найдёт его или создаст
            "contact": {"phone": lead["phone"], "name": lead["name"] or None},
            "external_id": external_id,
        })
        return deal, True
    except ConflictError as exc:
        if exc.code != "deal_exists":
            raise
        return client.deals.get(str(exc.details["deal_id"])), False


def greet(lead: dict[str, str]) -> Any:
    template: TemplateMessageIn = {"name": env("WAZZAPO_TEMPLATE_NAME"), "language": {"code": env("WAZZAPO_TEMPLATE_LANG", "ru")}}
    # Шаблон с {{1}} в тексте: подставляем имя клиента
    if env("WAZZAPO_TEMPLATE_NAME_PARAM") == "1":
        template["components"] = [{"type": "body", "parameters": [{"type": "text", "text": lead["name"] or "клиент"}]}]
    return client.messages.send({
        "phone_number_id": env("WAZZAPO_PHONE_NUMBER_ID"),
        "to": lead["phone"],
        "type": "template",
        "template": template,
    })


class Handler(BaseHTTPRequestHandler):
    def answer(self, status: int, body: dict[str, Any]) -> None:
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0)).decode()
        form = json.loads(raw or "{}") if "json" in (self.headers.get("Content-Type") or "") else dict(parse_qsl(raw))
        lead = {
            "name": str(form.get("name", "")).strip(),
            "phone": re.sub(r"\D+", "", str(form.get("phone", ""))),
            "comment": str(form.get("comment", "")).strip(),
            "lead_id": str(form.get("lead_id", "")).strip(),
        }
        if len(lead["phone"]) < 10:
            return self.answer(422, {"error": "Укажите телефон"})
        try:
            deal, created = deal_for(lead)
            out: dict[str, Any] = {"ok": True, "deal_id": deal["id"], "deal_number": deal["number"], "duplicate": not created}
            # Приветствие только новой заявке: повтор формы не шлёт клиенту второй шаблон
            if created and env("WAZZAPO_TEMPLATE_NAME"):
                out["message_id"] = greet(lead)["message_id"]
        except WazzapoError as exc:
            return self.answer(502, {"ok": False, "code": exc.code, "message": str(exc)})
        self.answer(200, out)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8081"))
    print("Приём заявок на порту", port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
