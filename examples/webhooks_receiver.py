"""Приёмник всех событий Wazzapo: проверяет подпись, сразу отвечает 200 и разбирает событие по типу.

Запуск: WAZZAPO_WEBHOOK_SECRET=... python webhooks_receiver.py
"""

from __future__ import annotations

import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from wazzapo import webhooks
from wazzapo.errors import WebhookVerificationError

SECRET = os.environ.get("WAZZAPO_WEBHOOK_SECRET")


def describe(event: Any) -> str:
    d = event["data"]
    kind = event["event"]
    if kind == "deal.stage_changed":
        deal = d.get("deal") or {}
        return f"Сделка {deal.get('number') or deal.get('id')}: этап «{(d.get('from_stage') or {}).get('name')}» → «{(d.get('to_stage') or {}).get('name')}»"
    if kind == "message.status":
        return f"Сообщение {d.get('message_id')}: {d.get('status')}"
    if kind == "message.incoming":
        message = d.get("message") or {}
        return f"Новое сообщение от {message.get('from')}: {message.get('text') or ''}"
    if kind == "deal.created":
        deal = d.get("deal") or {}
        return f"Новая сделка {deal.get('number') or deal.get('id')}"
    return f"Событие {kind}"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        payload = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        try:
            event = webhooks.verify(payload, self.headers, SECRET)
        except WebhookVerificationError as exc:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(exc).encode())
            return
        # Отвечаем сразу: долгая обработка до ответа приводит к повторной доставке
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')
        delivery = self.headers.get(webhooks.DELIVERY_ID_HEADER) or "-"
        threading.Thread(target=lambda: print(f"[wazzapo {delivery}]", describe(event), flush=True)).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8082"))
    print("Приёмник вебхуков на порту", port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
