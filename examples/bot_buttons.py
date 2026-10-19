"""Бот с кнопками: на входящее сообщение отвечает тремя кнопками, на нажатие кнопки отвечает текстом.

Запуск: WAZZAPO_API_KEY=... WAZZAPO_WEBHOOK_SECRET=... python bot_buttons.py
Адрес http(s)://ваш-сервер:8080/ укажите вебхуком на событие message.incoming.
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from wazzapo import Wazzapo, webhooks
from wazzapo.errors import WazzapoError, WebhookVerificationError

client = Wazzapo()
SECRET = os.environ.get("WAZZAPO_WEBHOOK_SECRET")
ANSWERS = {
    "prices": "Стрижка 5 000 ₸, окрашивание от 15 000 ₸. Записаться можно кнопкой «Записаться».",
    "book": "Отлично! Напишите удобный день и время, администратор подтвердит запись.",
    "manager": "Позвали администратора, он ответит в этом чате в течение 10 минут.",
}
# Повторы одной доставки: в памяти процесса; в работе храните в Redis или базе
seen: set[str] = set()


def reply(data: Any) -> Any:
    message = data["message"]
    phone_number_id, to = data["phone_number_id"], message["from"]
    pressed = message.get("interactive_reply_id")
    if pressed in ANSWERS:
        return client.messages.send(
            {"phone_number_id": phone_number_id, "to": to, "type": "text", "text": {"body": ANSWERS[pressed]}}
        )
    name = (data.get("contact") or {}).get("name")
    return client.messages.send({
        "phone_number_id": phone_number_id,
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": f"Здравствуйте{', ' + name if name else ''}! Чем помочь?"},
            "action": {"buttons": [
                {"type": "reply", "reply": {"id": "prices", "title": "Цены"}},
                {"type": "reply", "reply": {"id": "book", "title": "Записаться"}},
                {"type": "reply", "reply": {"id": "manager", "title": "Администратор"}},
            ]},
        },
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
        payload = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        try:
            event = webhooks.verify(payload, self.headers, SECRET)
        except WebhookVerificationError as exc:
            return self.answer(400, {"error": str(exc)})
        delivery_id = self.headers.get(webhooks.DELIVERY_ID_HEADER)
        if delivery_id in seen:
            return self.answer(200, {"ok": True, "duplicate": True})
        if delivery_id:
            seen.add(delivery_id)
        data = event["data"]
        # Только WhatsApp: у Telegram и чата на сайте свои правила кнопок
        if event["event"] != "message.incoming" or data.get("channel", "whatsapp") != "whatsapp":
            return self.answer(200, {"ok": True, "skipped": True})
        try:
            sent = reply(data)
        except WazzapoError as exc:
            # 200, чтобы Wazzapo не повторял доставку: ошибка отправки повтором вебхука не исправится
            self.log_message("Wazzapo: %s %s", exc.code, exc)
            return self.answer(200, {"ok": False, "code": exc.code})
        self.answer(200, {"ok": True, "message_id": sent["message_id"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print("Бот слушает порт", port)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
